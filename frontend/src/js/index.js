import {content_form_submit} from "/src/js/content.js";
import {login_form_submit} from "./login";
import {rich_text_area_loader} from "./rich_text";
import {
    editable_content_form_component, readonly_content_form_component,
    readonly_content_form_component_for_editor
} from "./html_components/content_form";
import {content_table_component, content_table_tr_component} from "./html_components/content_table";
import {login_form_component} from "./html_components/login_form";


const base_url = 'http://localhost:8000/';
const content_url = `${base_url}contents/api/v1/`;

const edit_content_button_handler = () => {
    const content = JSON.parse(localStorage.getItem('content'));
    const content_detail_url = `${content_url}${content.id}`;
    document.getElementById('included_content').innerHTML = editable_content_form_component(content);
    rich_text_area_loader();

    const content_form_element = document.getElementById('content_form');
    content_form_element.addEventListener('submit', async (event) => {
        event.preventDefault();
        await content_form_submit(content_detail_url, 'PATCH');
    });
}

const content_title_click_handler = (event) => {
    try {
        const content_id = event.target.getAttribute("data-content-id");
        if (content_id === null) throw new Error("Clicked at wrong place!");

        const included_content_element = document.getElementById('included_content');

        const content_details_url = `${content_url}${content_id}`;
        const other_params = localStorage.hasOwnProperty('token') ? {
            headers: {
                "Authorization": `JWT ${localStorage.getItem('token')}`
            }
        } : {};

        fetch(content_details_url, other_params).then(async response => {
            if (response.ok) {
                let content = await response.json();
                if (localStorage.hasOwnProperty('token')) {
                    included_content_element.innerHTML = readonly_content_form_component_for_editor(content);
                    document.getElementById("edit_content").addEventListener(
                        "click", edit_content_button_handler);
                    localStorage.setItem('content', JSON.stringify(content));
                }
                else included_content_element.innerHTML = readonly_content_form_component(content);
            } else {
                alert(await response.text());
            }
        });

        return false;
    } catch (error) {
        console.log(error);
    }
};

const content_table_loader = async () => {
    try {
        document.getElementById('included_content').innerHTML = content_table_component();
        const other_params = localStorage.hasOwnProperty('token') ? {
            headers: {
                "Authorization": `JWT ${localStorage.getItem('token')}`
            }
        } : {};

        fetch(content_url, other_params).then(async response => {
            if (response.ok) {
                let content_list = await response.json();
                console.log(content_list);

                let table_tbody = "";
                for (let content of content_list) {
                    document.getElementById("content_tbody").appendChild(
                        content_table_tr_component(content, content_title_click_handler)
                    );
                    // table_tbody += content_table_tr_component(content, "content_title_click_handler");
                }
                // document.getElementById("content_tbody").innerHTML = table_tbody;
            } else {
                alert(await response.text());
            }
        }).catch(function (error) {
            alert(error);
        });

        return false;
    } catch (error) {
        console.log(error);
    }
}

const auth_button_handler = () => {
    if (localStorage.getItem('token')) {
        localStorage.removeItem('token');
        document.getElementById('auth_button').innerHTML = "LOG IN";
        document.getElementById('create_content').style.display = "none";
    }
    // location.href = "/src/html/login.html";
    document.getElementById('included_content').innerHTML = login_form_component();
    const login_form_element = document.getElementById('login_form');
    login_form_element.addEventListener('submit', async (event) => {
        event.preventDefault();
        await login_form_submit();
    })
}

const create_content_button_handler = () => {
    document.getElementById('included_content').innerHTML = editable_content_form_component();
    rich_text_area_loader();

    const content_form_element = document.getElementById('content_form');
    content_form_element.addEventListener('submit', async (event) => {
        event.preventDefault();
        await content_form_submit(content_url, 'POST');
    });
}


window.addEventListener("load", async () => {
    let auth_button_element = document.getElementById('auth_button');
    let create_button_element = document.getElementById('create_content');

    if (localStorage.getItem('token')) {
        auth_button_element.innerHTML = "LOG OUT";
        create_button_element.style.display = "block";
    } else {
        auth_button_element.innerHTML = "LOG IN";
        create_button_element.style.display = "none";
    }

    // By default, content list would be displayed
    await content_table_loader();

    auth_button_element.addEventListener("click", auth_button_handler);

    create_button_element.addEventListener("click", create_content_button_handler);
});
