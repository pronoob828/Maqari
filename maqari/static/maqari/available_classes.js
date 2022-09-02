var current_page = 1

function load_halaqaat(page_no) {
    var halaqaat_container = document.querySelector('#halaqaat_container');
    document.querySelector('#page_no').innerHTML = `Page - ${current_page}`;
    halaqaat_container.innerHTML='';

    fetch(`show_available_classes/${page_no}`)
        .then(response => response.json())
        .then(halaqaat => {
            halaqaat.forEach(halaqa => {

               const teacher_desc = document.createElement('div');
               if(halaqa.teacher_years_of_experience > 0){
                var exp = `${halaqa.teacher_years_of_experience} years of experience <br>`
               }else{
                var exp = ``
               }
               teacher_desc.innerHTML = `
                            <img src="${halaqa.teacher_profile}" alt="Profile_image" class="img-thumbnail rounded-circle"><hr>
                        ${exp}
                        Current Residence - ${halaqa.teacher_current_residence}<br>
                        Nationality - ${halaqa.teacher_nationality}<br>
                        <small class="text-muted">Click for more info</small>                
                `;

                const halaqa_card = document.createElement('div');
                if (halaqa.is_enrolled) {
                    var enroll_button = `<button id="enroll_button_${halaqa.id}" class="btn btn-success disabled">Already enrolled</button>`;
                } else {
                    var enroll_button = `<button id="enroll_button_${halaqa.id}" class="btn btn-primary">Enroll</button>`;
                }

                halaqa_card.classList = "col";
                halaqa_card.innerHTML = `
                    <div class="card text-center">
                        <div id="${halaqa.halaqa_id}" class="card-body halaqa_link">
                            <img src="${halaqa.halaqa_image_url}" class="card-img-top styled_card_image"
                                alt="halaqa image">

                            <h5 class="card-title halaqa_info_button">
                            ${halaqa.halaqa_number} - ${halaqa.halaqa_type.type_name}
                                <button class="btn p-0" type="button" data-container="body" data-bs-toggle="popover" data-bs-trigger="hover" data-placement="bottom" title="${halaqa.halaqa_type.type_name}" data-bs-content="${halaqa.halaqa_type.type_desc}">
                                    <i class="fa-solid fa-circle-info mx-2"></i>
                                </button>
                            </h5>

                            <p class="card-text">
                            Teacher - 
                            <a href="accounts/profile/${halaqa.teacher_id}" data-bs-html="true" data-container="body" data-bs-toggle="popover" data-bs-trigger="hover" data-placement="top" title="${halaqa.teacher_name}" data-bs-content='${teacher_desc.innerHTML}'>${halaqa.teacher_name}</a>
                            </p>

                            <p class="card-text">Gender - ${halaqa.gender}.</p>
                            <p><small>Timings - ${halaqa.timings}<br>Students - ${halaqa.student_count}<br>
                            <small class="text-muted">Click card to view more</small>
                            </small></p>
                            
                        </div>
                        <div id="${halaqa.halaqa_id}" class="card-footer halaqa_link">` + enroll_button + `
                            </div>
                    </div>
                    `
                halaqaat_container.append(halaqa_card);

            });
        }).then(load_popper)
        .then(load_halaqa_links)
}

function load_popper() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
}

async function get_pages_count() {
    const response = await fetch("/get_page_count")
    const data = await response.json()
    const page_count = data["page_count"]
    return page_count
}

function load_halaqa_links(){
    const clickable = document.querySelectorAll('.halaqa_link')
    clickable.forEach(element => {
        element.addEventListener('click', function () {
            window.location.href = `halaqaat/${element.id}`
        });
    })
}

document.addEventListener('DOMContentLoaded', function () {
    
    load_halaqaat(current_page);    

    get_pages_count().then(pages_count => {
        document.querySelector("#prev_page").addEventListener("click", function () {
            if (current_page == 1) {
                return
            } else {
                current_page--
                load_halaqaat(current_page)
            }
        })

        document.querySelector("#next_page").addEventListener("click", function () {
            if (current_page == pages_count) {
                return
            } else {
                current_page++
                load_halaqaat(current_page)
            }
        })
    })


})