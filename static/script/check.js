let selected = []

const enforceBtn = document.querySelector('.enforceSelected');

checkboxes.forEach(c => c.addEventListener('change', ($event) => {
    index = Array.prototype.indexOf.call(checkboxes, $event.target);
    if (selected.includes(index))
        selected = selected.filter(i => i !== index);
    else
        selected.push(index);

    enforceBtn.disabled = selected.length < 1;
}));

enforceBtn.addEventListener('click', ($event) => {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/enforce', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = ($event) => {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200)
            console.log('enforced')
    }
    xhr.send(JSON.stringify(selected));
});

