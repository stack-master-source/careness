const get_sub_cards = async card_id => {
    let all_posts_modal = document.querySelector(".all-posts__modal"),
        order_card = document.querySelector(".order-card"),
        modal_sidebar = document.querySelector(".modal-sidebar");

    all_posts_modal.classList.add("show")
    modal_sidebar.innerHTML = "Данные загружаются..."

    await $.ajax({
        method: "GET",
        url: "/home/sub_cards/",
        headers: {"X-CSRFToken": CSRF},
        data: {"type": "page", "card_id": card_id}
    })
    .then(res => {
        if (res.success) {
            let data = res.data;
            modal_sidebar.innerHTML = `
                <span class="sidebar-close" onclick="close_modal();" style="cursor: pointer">
                    &#10230;
                </span>
                <h3 class="modal-sidebar__title">
                    Ответы
                </h3>
            `;

            data.forEach(element => {
                modal_sidebar.innerHTML += `
                    <div class="order-card">
                        <div class="order-card__left">
                            <p class="card-name">
                                ${ element["fields"]["user"]["fields"]["username"] }
                            </p>
                            <p class="card-location">
                                г. Тараз, iHerb.com
                            </p>
                            <img src="${DJANGO_STATIC_URL}/static/home/assets/drug.png" alt="" class="card-photo">
                        </div>
                        <div class="order-card__right">
                            <p class="card-number">
                                ${ element["fields"]["tel_number"] }
                            </p>
                            <p class="card-title">
                                ${ element["fields"]["name"] }
                            </p>
                            <a href=${ element["fields"]["product_link"] } class="card-link">
                                ${ element["fields"]["product_link"] }
                            </a>
                            <p class="card-amount">
                                <span class="red">Количество:</span> ${ element["fields"]["count"] }
                            </p>
                            <p class="card-description">
                                “${ element["fields"]["comment"] }”
                            </p>
                        </div>
                    </div>
                `;
            })
            modal_sidebar.innerHTML += `
                <button class="answer-announce" onclick="open_sub_card_model(${card_id});">
                    Откликнутся
                    <span class="iconify" data-icon="ri:send-plane-2-fill" data-inline="false"></span>
                </button>
            `;
        }
    })
    .catch(err => console.error(err))
}

const close_modal = () => {
    let all_posts_modal = document.querySelector(".all-posts__modal");
    all_posts_modal.classList.remove("show")
}

const close_modal_ = () => {
    let element_modal = document.querySelector(".modal");
    element_modal.classList.remove("show")
}

const open_sub_card_model = card_id => {
    let element_modal = document.querySelector(".modal"),
        modal_button = document.querySelector(".modal-button");

    element_modal.classList.add("show")
    modal_button.id = card_id;
}

const create_sub_card = async card_id => {
    let productname = document.querySelector("#productname").value,
        city = document.getElementById(`city_${ card_id }`).innerText,
        tel_number = document.querySelector("#tel_number").value,
        product_link = document.querySelector("#product_link").value,
        count = document.querySelector("#count").value,
        comment = document.querySelector("#comment").value,
        date = 0,
        modal = document.querySelector(".modal");

    await $.ajax({
        method: "POST",
        url: "/home/sub_cards/",
        headers: {"X-CSRFToken": CSRF},
        data: {
            "type": "create",
            "card_id": card_id,
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
    .then(res => res.success == 1 ? alert("Created successfully") : alert("Oops, something went wrong..."))
}