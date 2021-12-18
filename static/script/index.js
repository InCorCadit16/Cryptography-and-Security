
var selected = []
var allSelected = false;

const downloadBtn = document.querySelector('.downloadSelected');
const selectAllBtn = document.querySelector('.selectAll');
const testBtn = document.querySelector('.testSelected');
var checkboxes = document.querySelectorAll('[type=checkbox]');


checkboxes.forEach(c => c.addEventListener('change', ($event) => {
    index = Array.prototype.indexOf.call(checkboxes, $event.target);
    if (selected.includes(index))
        selected = selected.filter(i => i !== index);
    else
        selected.push(index);

    downloadBtn.disabled = selected.length < 1;
    testBtn.disabled = selected.length < 1;
}))


selectAllBtn.addEventListener('click', () => {
    if (allSelected) {
        checkboxes.forEach(c => c.checked=false);
        selected = [];
        selectAllBtn.innerText = 'Select All';
    } else {
        checkboxes.forEach(c => c.checked=true);
        selected = [...Array(checkboxes.length).keys()];
        selectAllBtn.innerText = 'Unselect All';
    }
    allSelected = !allSelected;
    downloadBtn.disabled = selected.length < 1;
    testBtn.disabled = selected.length < 1;
});


downloadBtn.addEventListener('click', () => {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/export', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = ($event) => {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200)
            downloadFile(xhr.response)
    }
    xhr.send(JSON.stringify(selected));
});

testBtn.addEventListener('click', () => {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/test', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*')
    xhr.onreadystatechange = ($event) => {
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            selected = []
            window.document.write(xhr.response)
        }

    }
    xhr.send(JSON.stringify(selected));
})




function downloadFile(data) {
    var file = new Blob([data], {type: 'application/json'});
    var a = document.createElement("a"),
    url = URL.createObjectURL(file);
    a.href = url;
    a.download = 'export.json';
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 0);
}