const create_card = async () => {
let productname = document.querySelector("#productname").value,
    city = document.querySelector("#city").value,
    tel_number = document.querySelector("#tel_number").value,
    product_link = document.querySelector("#product_link").value,
    count = document.querySelector("#count").value,
    comment = document.querySelector("#comment").value,
    date = document.querySelector("#date").value,
    modal = document.querySelector(".modal");

await $.ajax({
    method: "POST",
    url: "careness/home/cards/",
    headers: {"X-CSRFToken": CSRF},
    data: {
        "product_name": productname,
        "city": city,
        "product_link": product_link,
        "product_count": count,
        "date": date,
        "comment": comment,
        "count": count.length > 0 ? parseInt(count) : 0,
        "tel_number": tel_number
    }
})
.then(res => res.success == 1 ? alert("Card is created! please refresh the page") : alert("Oops, something went wrong..."))
.catch(err => console.error(err))
}