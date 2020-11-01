const display_modal = (card_id, type_) => {
    let element = document.querySelector(".modal");
    let modal_button = document.querySelector(".modal-button");
    element.classList.add("show")
    element.id = card_id
    modal_button.id = type_
}

const close_modal = () => {
    let element_modal = document.querySelector(".modal");
    element_modal.classList.remove("show")
}

const update_card = async type_ => {
    let productname = document.querySelector("#productname").value,
        city = document.querySelector("#city").value,
        tel_number = document.querySelector("#tel_number").value,
        product_link = document.querySelector("#product_link").value,
        count = document.querySelector("#count").value,
        comment = document.querySelector("#comment").value,
        date = document.querySelector("#date").value,
        modal = document.querySelector(".modal");

    if (type_ == "card") {
        await $.ajax({
            url: "/home/cards/edit/",
            method: "POST",
            headers: {"X-CSRFToken": CSRF},
            data: {
                "type": "update",
                "card_id": modal.id,
                "city": city,
                "comment": comment,
                "tel_number": tel_number,
                "product_name": productname,
                "product_link": product_link,
                "count": count.length > 0 ? parseInt(count) : 0,
                "comment": comment,
                "date": date,
            }
        })
        .then(res => res.success == 1 ? alert("Updated successfully") : alert("Something went wrong"))
        .catch(err => console.error(err));
    } else if (type_ == "sub_card") {
        await $.ajax({
            url: "/home/sub_cards/",
            method: "POST",
            headers: {"X-CSRFToken": CSRF},
            data: {
                "type": "update",
                "city": city,
                "tel_number": tel_number,
                "product_name": productname,
                "sub_card_id": modal.id,
                "product_link": product_link,
                "count": count.length > 0 ? parseInt(count) : 0,
                "comment": comment,
                "date": date,
            }
        })
        .then(res => res.success == 1 ? alert("Updated successfully") : alert("Something went wrong"))
        .catch(err => console.error(err));
    }
}

const delete_card = async card_id => {
    await $.ajax({
        method: "POST",
        url: "/home/cards/edit/",
        headers: {"X-CSRFToken": CSRF},
        data: {
            "type": "delete",
            "card_id": parseInt(card_id)
        }
    })
    .then(res => res.success == 1 ? alert("Deleted successfully") : alert("Oops, something went wrong!"))
    .catch(err => console.error(err))
}

const delete_sub_card = async card_id => {
    await $.ajax({
        method: "POST",
        url: "/home/sub_cards/",
        headers: {"X-CSRFToken": CSRF},
        data: {
            "type": "delete",
            "sub_card_id": parseInt(card_id)
        }
    })
    .then(res => res.success == 1 ? alert("Deleted successfully") : alert("Oops, something went wrong!"))
    .catch(err => console.error(err))
}