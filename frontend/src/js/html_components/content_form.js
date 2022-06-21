const rich_text_area = (text) => {
    return `
    <div class="text-editor-content">
        <div class="text-editor-header">
            <button type="button" class="editor-option-btn" data-element="bold">Bold</button>
            <button type="button" class="editor-option-btn" data-element="italic">Italic</button>
            <button type="button" class="editor-option-btn" data-element="createLink">Link</button>
            <button type="button" class="editor-option-btn" data-element="insertImage">Image</button>
            <button type="button" class="editor-option-btn" data-element="insertYoutube">YouTube</button>
        </div>
        <div class="text-editor-body" id="body" contentEditable="true">${text}</div>
    </div>
    `;
}

export const editable_content_form_component = (content = {}) => {
    return `
        <form id="content_form">
            <label for="title">Title:</label><br>
            <input type="text" id="title" name="title" required value="${content.title || ""}"><br>
            <label for="body">Body</label><br>
            ${rich_text_area(content.body || "")}
<!--            <textarea rows="20" cols="100" name="body" id="body" form="content_form" placeholder="Enter text here..." required>${content.body || ""}</textarea>-->
            <span id='message'></span>
            <input type="submit" value="Submit">
        </form>
    `;
}

export const readonly_content_form_component = (content) => {
    return `
        <form id="readonly_content_form">
            <span id="readonly_title">"${content.title}"</span><br>
            <span>Author: ${content.author}</span><br>
            <span>Created: ${content['created']}</span><br>
            <label for="body"></label><br>
            <div id="readonly_body">${content.body}</div><br>
        </form>
    `;
}

export const readonly_content_form_component_for_editor = (content) => {

    return `
        <form id="readonly_content_form">
            <span id="readonly_title">"${content.title}"</span><br>
            <span>Author: ${content.author}</span><br>
            <span>Created: ${content['created']}</span><br>
            <label for="body"></label><br>
            <div id="readonly_body">${content.body}</div><br>
            <button id="edit_content" data-content-id="${content.id}" style="margin-left: 50%;display: ${content['is_owner']? "block": "none"};">EDIT</button>
        </form>
    `;
}
