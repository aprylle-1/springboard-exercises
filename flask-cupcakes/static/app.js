// class Cupcake {
//     constructor(id, flavor, size, rating, image) {
//         this.id = id;
//         this.size = size;
//         this.rating = rating
//         this.flavor = flavor
//         this.image = image
//     }
// }

let cupcakeContainer = document.getElementById("cupcake-container")
let addCupcakeForm = document.getElementById("add-cupcake-form")
let btnShowAddCupcakeForm = document.getElementById("btn-show-modal")
let btnAddCupcake = document.getElementById("btn-add-cupcake")
let list_cupcakes = document.getElementById("cupcakes")
let closeCupcakeForm = document.getElementById("close-cupcake-form")

const get_all_cupcakes = async function () {
    cupcakes = await axios.get("/api/cupcakes")
    data = cupcakes
    return data
}

async function init () {
    list_cupcakes.innerText = ""
    cupcakes = await get_all_cupcakes()
    
    for (let cupcake of cupcakes.data.cupcakes) {
        let div = create_card(cupcake)
        list_cupcakes.append(div)
    }
}

function create_card(data) {
    let div = document.createElement("div")
    div.classList.add("card")

    let img = document.createElement("img")
    img.classList.add("card-img-top")
    img.src = data.image
    div.append(img)

    let ul = document.createElement("ul")
    ul.classList.add("list-group") 
    ul.classList.add("list-group-flush")

    let li_flavor = document.createElement("li")
    li_flavor.classList.add("list-group-item")
    li_flavor.innerText = `Flavor: ${data.flavor}` 
    ul.append(li_flavor)

    let li_size = document.createElement("li")
    li_size.classList.add("list-group-item")
    li_size.innerText = `Size: ${data.size}`
    ul.append(li_size)

    let li_rating = document.createElement("li")
    li_rating.classList.add("list-group-item")
    li_rating.innerText = `Rating: ${data.rating}`
    ul.append(li_rating)

    div.append(ul)

    return div
}

async function addCupcake() {
    
    let flavor = document.getElementById("flavor").value
    let size = document.getElementById("size").value
    let rating = document.getElementById("rating").value
    let image = document.getElementById("image").value

    let resp = await axios.post("/api/cupcakes", {
        flavor,
        size,
        rating,
        image
    })

    addCupcakeForm.classList.toggle("shown")
    cupcakeContainer.classList.toggle("blur")

    div = create_card(resp.data.cupcake)
    list_cupcakes.append(div)
}

btnAddCupcake.addEventListener("click", async function(e) {
    e.preventDefault()
    resp = await addCupcake()
})

btnShowAddCupcakeForm.addEventListener("click", function(e) {
    e.preventDefault()

    cupcakeContainer.classList.add("blur")

    addCupcakeForm.classList.add("shown")
})

closeCupcakeForm.addEventListener("click", function(e){
    e.preventDefault()

    cupcakeContainer.classList.toggle("blur")
    
    addCupcakeForm.classList.toggle("shown")
})

init()
