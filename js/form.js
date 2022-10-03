let url = "https://raw.githubusercontent.com/sujaldev/JEEPYQREPLYBOT/master/src/data.json";
let data = {}
let subject_select_tag;
let topic_select_tag;
let option_group;
let option_number = 1;
let add_option_btn;


async function syncData() {
    data = await (await fetch(url).then(r => r.json()));
}

syncData().then(
    () => {
        subject_select_tag = document.querySelector("#subject-selection");
        topic_select_tag = document.querySelector("#topic-selection");
        option_group = document.querySelector("#option-group");
        add_option_btn = document.querySelector("#add-option-btn");
        setSubjects();
    }
)

function setSubjects() {
    for (const subject of Object.keys(data)) {
        let option_tag = document.createElement("option")
        option_tag.setAttribute("value", subject)
        option_tag.innerText = subject
        subject_select_tag.appendChild(option_tag);
    }

    subject_select_tag.addEventListener("change", setTopics)
}

function setTopics() {
    let topics = Object.keys(data[subject_select_tag.value]);
    topic_select_tag.innerHTML = "";
    for (const topic of topics) {
        let option_tag = document.createElement("option")
        option_tag.setAttribute("value", topic)
        option_tag.innerText = topic
        topic_select_tag.appendChild(option_tag)
    }
}


function generateOptionElement() {
    // Create parent container
    let container = document.createElement("div")
    container.setAttribute("class", "option")

    // Create checkbox input label
    let checkbox_label = document.createElement("label")
    checkbox_label.setAttribute("for", `option-${option_number}-correct`)
    checkbox_label.innerHTML = `Option ${option_number}: &nbsp; `
    container.appendChild(checkbox_label)

    // Create checkbox input
    let checkbox_input = document.createElement("input")
    checkbox_input.setAttribute("type", "checkbox")
    checkbox_input.setAttribute("name", `option[${option_number}][correct]`)
    checkbox_input.setAttribute("id", `option-${option_number}-correct`)
    container.appendChild(checkbox_input)

    // Create horizontal line
    let hr = document.createElement("hr")
    container.appendChild(hr)

    // Create text input label
    let text_label = document.createElement("label")
    text_label.setAttribute("for", `option-${option_number}-text`)
    text_label.innerHTML = "Enter the option text: "
    container.appendChild(text_label)

    // Create checkbox input
    let text_input = document.createElement("textarea")
    text_input.setAttribute("name", `option[${option_number}][text]`)
    text_input.setAttribute("id", `option-${option_number}-text`)
    text_input.setAttribute("placeholder", "Try to keep the text on a single line")
    container.appendChild(text_input)

    // Append container to option group
    option_group.appendChild(container)

    // increment option number
    option_number++;
}