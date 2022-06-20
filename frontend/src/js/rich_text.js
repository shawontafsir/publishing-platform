const isUrl = string => {
    try { return Boolean(new URL(string)); }
    catch(e){ return false; }
}

function createHtmlElementFromHTMLString(htmlString) {
    const div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    // Change this to div.childNodes to support multiple top-level nodes.
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

        // document.getElementById(containerId).focus();
        // if the range is in selected node
        // if (range.startContainer.id === containerId) {
        // delete whatever is on the range
        range.deleteContents();
        // place your span
        range.insertNode(htmlElement);
        // }
    } catch (error) {
        console.log(error);
    }
}

const insertImage = function () {
    const url = prompt("Enter the link here");
    if (!isUrl(url)) return;

    const embed = `<embed title="Image" src="${url}"  width="40%" height="40%">`;
    pasteHtmlElementAtCaret(createHtmlElementFromHTMLString(embed), "body");
    // document.getElementById('body').appendChild(createElementFromHTML(embed));
    // document.execCommand("insertHtml", false, embed);
}

const insertYoutube = function () {
    const url = prompt("Enter the link here");
    if (!isUrl(url)) return;

    const urlReplace = url.replace("watch?v=", "embed/");
    console.log(urlReplace);
    const embed = '<embed title="YouTube video player" src="' + urlReplace + '"  width="40%" height="80%">Alt</embed>';
    // document.getElementById('body').appendChild(createElementFromHTML(embed));
    console.log(embed);
    pasteHtmlElementAtCaret(createHtmlElementFromHTMLString(embed), "body");
}

export const rich_text_area_loader = () => {
    const elements = document.querySelectorAll('.editor-option-btn');

    console.log(elements);

    for (let element of elements) {
        element.addEventListener("click", () => {
            let command = element.dataset['element'];
            console.log(command);

            if (command === "createLink") {
                let url = prompt("Enter the link here") || "";
                console.log(url);
                document.execCommand(command, false, url);
            } else if (command === "insertImage") insertImage();
            else if (command === "insertYoutube") insertYoutube();
            else document.execCommand(command, false, null);
        });
    }
}
