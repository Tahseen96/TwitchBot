function running() {
    console.log('clicked')
    mainButton.removeEventListener('click', running, true)

    desc = document.querySelector('.description')
    descs = ["Running.", "Running..", "Running..."]
    desc_index = 0
    setInterval(()=>{
        desc_index = (desc_index + 1) % 3
        desc.innerText = descs[desc_index]
    }, 500)
    eel.run_main()
}
let mainButton = document.querySelector('#mainButton')
mainButton.addEventListener('click', running, true)
console.log("script")
eel.expose(add_new_to_cooldown)
function add_new_to_cooldown(){
    _in = document.querySelector('span.in')
    total = document.querySelector('span.total')
    _in.innerText = parseInt(_in.innerText) + 1
    total.innerText = parseInt(total.innerText) + 1
}
eel.expose(remove_from_cooldown)
function remove_from_cooldown(){
    _in = document.querySelector('span.in')
    _in.innerText = parseInt(_in.innerText) - 1
}