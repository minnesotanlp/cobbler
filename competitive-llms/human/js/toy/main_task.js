    let collectedData_task = [];
    let currentPage_task = 1;

    // function shuffleArray(array) {
    //     for (let i = array.length - 1; i > 1; i--) {
    //         const j = Math.floor(Math.random() * (i + 1));
    //         if (j != 0) { 
    //             [array[i], array[j]] = [array[j], array[i]];
    //         }
    //     }
    //     console.log(array)
    //     return array;
    // }

    // function removeItemFromArray(array, item){
    //     let index = array.indexOf(item);
    //     if (index !== -1) {
    //         array.splice(index, 1);
    //     }
    //     return array;
    // }

    function renderExamples_task() {
        const start = (currentPage_task - 1) * pageSize;
        console.log('rendering example task')
        const end = currentPage_task * pageSize;
        const currentExamples_task = examples_task.slice(start, end);
        let numMethods = 0;

        const exampleContainer_task = $("#example-container-task");
        exampleContainer_task.empty();

        currentExamples_task.forEach((example, index) => {
            const exampleIndex = start + index;
            
            let savedMethods = null;
            let savedRanking = null;
            if (window.localStorage) {
                const savedData = localStorage.getItem(`example-${exampleIndex}`);
                if (savedData) {
                    const parsedData = JSON.parse(savedData);
                    savedMethods = parsedData.methods;
                    savedRanking = parsedData.ranking;
                }
            }
            var methodsNames = Object.keys(example);
            methodsNames = removeItemFromArray(methodsNames, "instruction");
            methodsNames = removeItemFromArray(methodsNames, "reference");
            methodsNames = removeItemFromArray(methodsNames, "gold_label");
            methodsNames = removeItemFromArray(methodsNames, "contrast_label");

            const numMethods = methodsNames.length;
            const methodsRanking = Array(numMethods).fill().map((_, i) => i+1);
            if(shuffleMethods){
                methodsNames = shuffleArray(methodsNames);
            }
            const randomizedMethods = savedMethods || methodsNames;
            const randomizedRanking = savedRanking || methodsRanking;
           

            let className = "methodAnon";
            let exampleHtml = ``;
            if(showReferences){
                exampleHtml += `<div class="container instruction"><div class="p-2 rounded">`
                exampleHtml += `<span class="badge bg-secondary text-light text-uppercase">Instruction</span><br /> `
                if(showGoldLabels) {
                    gold_label = example['gold_label'] || 'Reference';
                    exampleHtml += `<span class="badge bg-secondary text-light text-uppercase">` + gold_label + `</span><br />`
                }
                exampleHtml += (example['instruction'] + `</div></div>`);
                
                exampleHtml += `<div class="container reference"><div class="p-3 rounded">`
                exampleHtml += `<span class="badge bg-secondary text-light text-uppercase">Reference</span><br /> `
                exampleHtml += (example['reference'] + `</div></div>`);
            }
            exampleHtml += `<div class="container example">`;
            exampleHtml += `<ul class="list-group sortable" data-example-index="` + exampleIndex + `">`;

            // exampleHtml += `
            //     <li class="list-group-item black-bar" data-method="black-bar">
            //         <div class="row">
            //             <div class="col-xs-auto"><span class="rank-number badge rounded-pill text-light"></span></div>
            //             <div class="col black-bar-content"></div>
            //         </div>
            //     </li>`;

            randomizedMethods.forEach((method, idx) => {
                if(colorizeBoxes){
                    if(colorizePerMethod){
                        className = method;
                    }
                    else{
                        className = "method" + idx;
                    }
                }
                if(useDraggableInterface) {
                    if (method == "black-bar") {
                        exampleHtml += `
                            <li class="list-group-item black-bar" data-method="black-bar">
                                <div class="row">
                                    <div class="col black-bar-content"></div>
                                </div>
                            </li>`;
                    } else {
                        exampleHtml += '<li class="list-group-item ' + className + '" data-method="' + method + '">';
                        exampleHtml += '    <div class="row">';
                        exampleHtml += '        <div class="col-xs-auto"><span class="rank-number badge rounded-pill text-light">'+ method + '</span></div>';
                        exampleHtml += '        <div class="col">';
                        exampleHtml += '            ' + example[method] + '</div>';
                        exampleHtml += '        </div>';
                        exampleHtml += '</li>';
                    }
                }
                else {
                    exampleHtml += `
                        <li class="list-group-item ` + className + `" data-method="` + method + `">
                            <div class="row">
                                <div class="col-xs-auto">
                                    <input type="text" class="form-control form-control-sm rank-number-input rounded text-light" value="` + randomizedRanking[idx] + `" />
                                </div>
                                <div class="col">` + example[method] + `</div>
                            </div>
                        </li>`;
                }
            });
            exampleHtml += `</ul></div>`;
            exampleContainer_task.append(exampleHtml);

            handleRanking(exampleIndex, randomizedMethods, randomizedRanking);
        });


        if(useDraggableInterface) {
            $(".sortable").sortable({
                stop: function (event, ui) {
                    const exampleIndex = $(this).data("example-index");
                    // $(this).find('span').each(function(idx){
                    //     $(this).html(idx + 1);
                    // });
                    let methods = $(this).find('.list-group-item').map(function(){
                        return $(this).data('method');
                    }).get();
                    let ranking = $(this).find('.rank-number').map(function(){
                        return parseInt($(this).html());
                    }).get();
                    handleRanking(exampleIndex, methods, ranking);
                },
            });
        }
        else {
            $(".example .rank-number-input").on("change", function (e) {
                let val = parseInt($(this).val());
                let example = $(this).closest(".list-group");
                let exampleIndex = example.data("example-index");
                let methods = example.find('.list-group-item').map(function(){
                    return $(this).data('method');
                }).get();
                let ranking = example.find('.rank-number-input').map(function(){
                    return $(this).val();
                }).get();
                
                if(val < 1 || val > methods.length){
                    $(this).css("border", "2px solid #E66465");
                }
                else{
                    $(this).css("border", "0px");
                    handleRanking(exampleIndex, methods, ranking);
                }
            });
        }
    }

    function handleRanking(exampleIndex, methods, ranking) {
        const data = {
            exampleIndex: exampleIndex,
            methods: methods,
            ranking: ranking,
            timestamp: new Date().toISOString(),
        };
        collectedData_task[exampleIndex] = data;

        // Save data to a local file asynchronously
        if (window.localStorage) {
            const key = `example-${exampleIndex}`;
            const value = JSON.stringify(data);
            localStorage.setItem(key, value);
        } else {
            console.error("Local storage is not supported by your browser.");
        }
    }
    
    function saveToTurker() {
        const jsonData_toy = JSON.stringify(collectedData_toy);
        const inputElement_toy = document.getElementById('jsonDataInput-toy');
        inputElement_toy.value = jsonData_toy;

        const jsonData_task = JSON.stringify(collectedData_task);
        const inputElement_task = document.getElementById('jsonDataInput-task');
        inputElement_task.value = jsonData_task;
    }

    function renderPagination_task() {
        const totalPages_task = Math.ceil(examples_task.length / pageSize);
        const pagination_task = $("#pagination-task");
        pagination_task.empty();

        for (let i = 1; i <= totalPages_task; i++) {
            const pageItem = $(`<li class="page-item"><a class="page-link" href="#page=` + i + `">` + i + `</a></li>`);
            if (i === currentPage_task) {
                pageItem.addClass("active");
            }
            pagination_task.append(pageItem);
        }

        $(".page-link").on("click", function (e) {
            localStorage.clear();
            e.preventDefault();
            currentPage_task = parseInt($(this).text());
            renderExamples_task();
            renderPagination_task();
            window.location.hash = `page=` + currentPage_task;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    function init_task() {
        console.log('running init_task')
        // localStorage.clear();
        renderExamples_task();
        renderPagination_task();

        // Initialize event listeners for ranking and pagination...
        $("#save-button").on("click", saveToTurker);
    }

    // init_task();


    function run_task() {
        document.getElementById('toy_page').style.display = "none";
        document.getElementById('task_page').style.display = "";
        const messageContainer = document.getElementById("task_page_head");
        messageContainer.innerHTML = `
    
        <br><h2>Task Session</h2>
        <br>
        <p> You are given the following five examples. Unlike toy session, there is no "correct answer." Please provide your own insights into ranking those examples based on your preference. </p>
        <p> <b style='color:red'> Warning: </b> <b>Please make sure to click each page button more than twice before you start</b>. There is a likely technical bug in the interface. </p>

        `
        init_task();
    }
    
    // run_task();