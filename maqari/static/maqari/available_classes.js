var current_page = 1

function load_halaqaat(page_no) {
    var halaqaat_container = document.querySelector('#halaqaat_container');
    document.querySelector('#page_no').innerHTML = `Page - ${current_page}`;

    fetch(`show_available_classes/${page_no}`)
        .then(response => response.json())
        .then(halaqaat => {
            halaqaat.forEach(halaqa => {
                const halaqa_card = document.createElement('div');
                if(halaqa.is_enrolled){
                    var enroll_button = `<button id="enroll_button_${halaqa.id}" class="btn btn-success disabled">Already enrolled</button>`;
                }else{
                    var enroll_button = `<button id="enroll_button_${halaqa.id}" class="btn btn-primary">Enroll</button>`;
                }
                
                halaqa_card.classList = "col";
                halaqa_card.innerHTML = `
                    <div class="card text-center">
                        <div class="card-body">
                            <img src="${halaqa.halaqa_image_url}" class="card-img-top"
                                alt="halaqa image" style="width:100%!important;height:300px!important;object-fit:cover">
                            <h5 class="card-title halaqa_info_button">${halaqa.halaqa_number} - ${halaqa.halaqa_type.type_name}<button class="btn p-0" type="button" data-container="body" data-bs-toggle="popover" data-placement="bottom" title="${halaqa.halaqa_type.type_name}" data-bs-content="${halaqa.halaqa_type.type_desc}"><i class="fa-solid fa-circle-info mx-2"></i></button></h5>
                            <p class="card-text">Teacher - <a
                                    href="accounts/profile/${halaqa.teacher_id}">${halaqa.teacher_name}</a></p>
                            <p class="card-text">Gender - ${halaqa.gender}.</p>
                            <p><small>Timings - ${halaqa.timings}</small></p>
                            <div class="card-footer">` + enroll_button + `
                            </div>
                        </div>
                    </div>
                    `
                halaqaat_container.append(halaqa_card);
                
            });
        })

}

document.addEventListener('DOMContentLoaded', function () {
    load_halaqaat(current_page);
})