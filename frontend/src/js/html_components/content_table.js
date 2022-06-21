export const content_table_component = () => {
    return `
        <table id="content_table">
            <caption>Table: Content List</caption>
            <thead>
                <th>Title</th>
                <th>Creation Date</th>
                <th>Author</th>
            </thead>
            <tbody id="content_tbody">
                <tr></tr>
            </tbody>
        </table>
    `;
}

export const content_table_tr_component = (content, handler) => {
    let template = document.createElement('template');
    template.innerHTML = `<tr>
            <td><a href="#" data-content-id="${content.id}">${content.title}</a></td>
            <td>${new Date(content.created).toLocaleString()}</td>
            <td style="width: 10%">${content.author}</td>
            </tr>`;
    const firstNode = template.content.firstElementChild.cloneNode(true);
    firstNode.addEventListener('click', handler);
    return firstNode;
}
