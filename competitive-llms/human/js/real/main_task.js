
    // let useDraggableInterface = $('#interface-type').val() === "draggable";
    const useDraggableInterface = true;

    const colorizeBoxes = true;
    const colorizePerMethod = true;
    const showReferences = true;
    const shuffleMethods = false;
    const showGoldLabels = false;
    const pageSize = 1;
        
    let collectedData_toy= [];
    let currentPage_toy = 1;
    
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 1; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            if (j != 0) { 
                [array[i], array[j]] = [array[j], array[i]];
            }
        }
        return array;
    }

    function removeItemFromArray(array, item){
        let index = array.indexOf(item);
        if (index !== -1) {
            array.splice(index, 1);
        }
        return array;
    }

    function renderExamples_toy() {
        const start = (currentPage_toy - 1) * pageSize;
        console.log('rendering example toy')
        const end = currentPage_toy * pageSize;
        const currentExamples_toy = examples_toy.slice(start, end);
        let numMethods = 0;

        const exampleContainer_toy = $("#example-container-toy");
        exampleContainer_toy.empty();

        currentExamples_toy.forEach((example, index) => {
            console.log(example)
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
            let exampleHtml_toy = ``;
            if(showReferences){
                exampleHtml_toy += `<div class="container instruction"><div class="p-2 rounded">`
                exampleHtml_toy += `<span class="badge bg-secondary text-light text-uppercase">Instruction</span><br /> `
                if(showGoldLabels) {
                    gold_label = example['gold_label'] || 'Reference';
                    exampleHtml_toy += `<span class="badge bg-secondary text-light text-uppercase">` + gold_label + `</span><br />`
                }
                exampleHtml_toy += (example['instruction'] + `</div></div>`);
                
                exampleHtml_toy += `<div class="container reference"><div class="p-3 rounded">`
                exampleHtml_toy += `<span class="badge bg-secondary text-light text-uppercase">Reference</span><br /> `
                exampleHtml_toy += (example['reference'] + `</div></div>`);
            }
            exampleHtml_toy += `<div class="container example">`;
            exampleHtml_toy += `<ul class="list-group sortable" data-example-index="` + exampleIndex + `">`;

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
                        exampleHtml_toy += `
                            <li class="list-group-item black-bar" data-method="black-bar">
                                <div class="row">
                                    <div class="col black-bar-content"></div>
                                </div>
                            </li>`;
                    } else {
                        exampleHtml_toy += '<li class="list-group-item ' + className + '" data-method="' + method + '">';
                        exampleHtml_toy += '    <div class="row">';
                        exampleHtml_toy += '        <div class="col-xs-auto"><span class="rank-number badge rounded-pill text-light">'+ method + '</span></div>';
                        exampleHtml_toy += '        <div class="col">';
                        exampleHtml_toy += '            ' + example[method] + '</div>';
                        exampleHtml_toy += '        </div>';
                        exampleHtml_toy += '</li>';
                    }
                }
                else {
                    exampleHtml_toy += `
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
            exampleHtml_toy += `</ul></div>`;
            exampleContainer_toy.append(exampleHtml_toy);

            handleRanking_toy(exampleIndex, randomizedMethods, randomizedRanking);
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
                    handleRanking_toy(exampleIndex, methods, ranking);
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
                    handleRanking_toy(exampleIndex, methods, ranking);
                }
            });
        }
    }

    function handleRanking_toy(exampleIndex, methods, ranking) {
        const toy_data = {
            exampleIndex: exampleIndex,
            methods: methods,
            ranking: ranking,
            timestamp: new Date().toISOString(),
        };
        collectedData_toy[exampleIndex] = toy_data;

        // Save data to a local file asynchronously
        if (window.localStorage) {
            const key = `example-` +exampleIndex;
            const value = JSON.stringify(toy_data);
            localStorage.setItem(key, value);
        } else {
            console.error("Local storage is not supported by your browser.");
        }
    }
    
    function saveToTurker_toy() {
        const jsonData = JSON.stringify(collectedData_toy);
        const inputElement = document.getElementById('jsonDataInput-toy');
        inputElement.value = jsonData;
    }

    function renderPagination_toy() {
        const totalPages_toy = Math.ceil(examples_toy.length / pageSize);
        const pagination_toy = $("#pagination-toy");
        pagination_toy.empty();

        for (let i = 1; i <= totalPages_toy; i++) {
            const pageItem_toy = $(`<li class="page-item"><a class="page-link" href="#page=` + i + `">` + i + `</a></li>`);
            if (i === currentPage_toy) {
                pageItem_toy.addClass("active");
            }
            pagination_toy.append(pageItem_toy);
        }

        $(".page-link").on("click", function (e) {
            localStorage.clear();
            e.preventDefault();
            currentPage_toy = parseInt($(this).text());
            renderExamples_toy();
            renderPagination_toy();
            window.location.hash = `page=` + currentPage_toy;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
 
    function init_toy() {

        renderExamples_toy();
        renderPagination_toy();

        // Initialize event listeners for ranking and pagination...
        $("#task-button").on("click", saveToTurker_toy);
    }

    // init_toy();


function run_toy() {
    document.getElementById('instruction_page').style.display = "none";
	document.getElementById('toy_page').style.display = "";
	const messageContainer = document.getElementById("toy_page_head");
	messageContainer.innerHTML = `

	<br><h2>Work Session</h2> <br>
	<h4> Please rank the examples as given below. Your answers will be <b style="color:red">checked later for the approval</b> and for the <b style="color:red">qualification to the next task.</b>. </h4> 
    <hr>
    <p> Your task is to <b>rank those AI-generated answers by your preference,</b> in terms of the following points:
    <ul>
        <li>(1) which answer sounds better <b>fluent</b> and <b>reasonable</b> with respect to the instruction question, and </li> 
        <li>(2) which answer <b style='color:red'>aligns better</b> with the reference sentence. (Please note that the reference answer is one possible answer to the instruction question.) </li>
    </ul>
    <p>
    To rank outputs, <b style="color:blue">follow these steps: </b> <br>
    <ol>
        <li> Read thoughtfully each of answers in the stack. </li>
        <li> Rank the quality of answer by each system from the top to the bottom, by <b style="color:red">dragging and dropping the system with most quality of answer to the top, 
        followed by the second most one, and so on. </b> Then, you will place the least to the bottom. 
        Note that you can always swap a former answer that have been rated with the latter one, if the latter sounds better. </li>
        <li> <b style="color:red">[IMPORTANT]</b> Drag and drop <b>the black bar</b> <b style="color:red">right above</b> the answer(s) that is not relevant to the instruction/reference sentences and does not sound reasonable. The bar works as a "threshold", which means that
        <b>the answers below the black bar</b> will be considered as <b style="color:blue"><i>"non-reasonble" and "irrelevant"</i></b>. If you think all answers sound good, then you may place the black bar at the most bottom.</li>
        <li>After ranking all answers, then click to the <b style="color:blue">next page</b>. </li>
    </ol>
    </p>
    <br>
    <p> <b style='color:red'> Warning: </b> <b>Please only click Submit Results button when you finish ranking all examples in the last page</b>. </p>
    <br>
    `
	init_toy();
}


// run_toy();
