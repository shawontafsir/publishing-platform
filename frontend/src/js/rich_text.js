const isUrl = string => {
    try {
        return Boolean(new URL(string));
    }
    catch(error){
        return false;
    }
}

function createHtmlElementFromHTMLString(htmlString) {
    const div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    return div.firstChild;
}

function pasteHtmlElementAtCaret(htmlElement, containerId) {
    try {
        let userSelection;
        if (window.getSelection) {
            userSelection = window.getSelection();
        } else if (document.selection) {
            userSelection = document.selection.createRange();
        }
        console.log(userSelection);
        const anchor = userSelection.anchorNode;
        const parent = anchor.parentElement;
        if (anchor.id !== containerId &&
            (parent && parent.id !== containerId) &&
            (parent && parent.parentElement.id !== containerId)) throw new Error("Wrong place to select!")

        // get the selection range (or cursor position)
        let range = userSelection.getRangeAt(0);

        // if the range is in selected node
        // if (range.startContainer.id === containerId) {
        // delete whatever is on the range
        range.deleteContents();
        // place your span
        range.insertNode(htmlElement);
    } catch (error) {
        console.log(error);
    }
}

const insertImage = function () {
    const url = prompt("Enter the link here");
    if (!isUrl(url)) return;

    const embed = `<embed title="Image" src="${url}"  width="40%" height="40%">`;
    pasteHtmlElementAtCaret(createHtmlElementFromHTMLString(embed), "body");
}

const insertYoutube = function () {
    const url = prompt("Enter the link here");
    if (!isUrl(url)) return;

    const urlReplace = url.replace("watch?v=", "embed/");
    const embed = '<embed title="YouTube video player" src="' + urlReplace + '"  width="40%" height="80%">Alt</embed>';
    pasteHtmlElementAtCaret(createHtmlElementFromHTMLString(embed), "body");
}

export const rich_text_area_loader = () => {
    const elements = document.querySelectorAll('.editor-option-btn');

    for (let element of elements) {
        element.addEventListener("click", () => {
            let command = element.dataset['element'];

            if (command === "createLink") {
                let url = prompt("Enter the link here") || "";
                document.execCommand(command, false, url);
            } else if (command === "insertImage") insertImage();
            else if (command === "insertYoutube") insertYoutube();
            else document.execCommand(command, false, null);
        });
    }
}
