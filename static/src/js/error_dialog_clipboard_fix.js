/** @odoo-module **/

/**
 * Patch Odoo error dialogs so the "Copy" button works when navigator.clipboard
 * is undefined (e.g. on HTTP). Uses execCommand('copy') as fallback.
 */
import { patch } from "@web/core/utils/patch";
import { ErrorDialog, RPCErrorDialog } from "@web/core/errors/error_dialogs";

function safeCopyToClipboard(text) {
    const clip = typeof navigator !== "undefined" && navigator.clipboard;
    if (clip && typeof clip.writeText === "function") {
        return clip.writeText(text);
    }
    // Fallback for non-secure contexts (HTTP)
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try {
        document.execCommand("copy");
        return Promise.resolve();
    } finally {
        document.body.removeChild(ta);
    }
}

patch(ErrorDialog.prototype, {
    onClickClipboard() {
        const text = `${this.props.name}\n\n${this.props.message}\n\n${this.contextDetails}\n\n${this.props.traceback}`;
        safeCopyToClipboard(text).then(
            () => this.showTooltip(),
            () => {}
        );
    },
});

patch(RPCErrorDialog.prototype, {
    onClickClipboard() {
        const text = `${this.props.name}\n\n${this.props.message}\n\n${this.contextDetails}\n\n${this.traceback}`;
        safeCopyToClipboard(text).then(
            () => this.showTooltip(),
            () => {}
        );
    },
});
