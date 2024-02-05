function show_task_answer(button_id, text_id, text){

  console.log(encodeURIComponent(text));

  var decode_text = decodeURIComponent(text);
  decode_text = decode_text.replace(/%0A/g, '<br>');
  const button = document.getElementById(button_id);
  const output = document.getElementById(text_id);
  console.log(decode_text)

  button.addEventListener("click", function() {
      output.innerHTML = decode_text;
      output.style.display = "";
      output.style.borderStyle = "dotted";
      output.style.borderColor = "orange";
      output.style.padding = "10px";
  });
}

let currentPage = 0;

function startPages() {

    // Initialize pages
    A.forEach((data, index) => {
      loadPage(data, index);
    });

    // Show the first page
    showPage(currentPage);
  }

  function loadPage(data, index) {
    const contentDiv = document.createElement('div');
    contentDiv.id = "page_"+index;
    contentDiv.style.display = "none"; // Hidden by default
    contentDiv.innerHTML =     '<h3> Question Set ' + (index + 1) + ' out of ' + A.length + '</h3>' +
    '<br>' +
    '<div id="task_' + (index + 1) + '" style="border-style: dotted; border-color: CornflowerBlue; padding: 10px; color:black">' +
      '<p>### <b> Question: </b> Which system\'s answer is <b style=\'color:SlateBlue\'>more coherent</b>, considering the reference and instruction sentences? </p>' +
      '<ul>' +
        '<li> <b>The instruction</b>: <span id="instruction_' + (index + 1) + '">' + data.instruction + '</span> </li>' +
        '<li> <b>The reference</b>: <span id="reference_' + (index + 1) + '">' + data.reference + '</span></li>' +
      '</ul>' +
      '<div id="systemA" class="mt-3" style="text-align:center;">' +
        '<p> First, Double-Click <b>System A</b> button to see the A\'s answer. </p>' +
        '<label id="task_' + (index + 1) + '_buttonA" class="btn btn-success">'
          + 'System A' + '</label>' +
        '<div id="task_' + (index + 1) + '_systemA_answer" class="mt-3"></div>' +
      '</div>' + 
      '<br>' +
      '<div id="systemB" class="mt-3" style="text-align:center;">' +
        '<p> And then, Double-Click <b>System B</b> button to see the B\'s answer. </p>' +
        '<label id="task_' + (index + 1) + '_buttonB" class="btn btn-info">'
          + 'System B' + '</label>' +
        '<div id="task_' + (index + 1) + '_systemB_answer" class="mt-3"></div>' +
      '</div>' + 
      '<br><br>' +
      '<p style="text-align: center">' +
      '<mark>' +
      'Please choose which system\'s answer aligns and cohere better with the instruction and reference sentences?' +
      '</mark>' +
      '</p>' +
      '<div style="text-align: center">' +
        '<label class="btn btn-success btn-lg" style="margin-right: 20px;">' +
          '<input type="radio" id="radioA_' + (index + 1) + '" name="task_' + (index + 1) + '" value="A"> System A' +
        '</label>' +
        '<label class="btn btn-info btn-lg">' +
          '<input type="radio" id="radioB_' + (index + 1) + '" name="task_' + (index + 1) + '" value="B"> System B' +
        '</label>' +
      '</div>' +
    '</div>';
    
    // Create a new div for this page
    if (index != (A.length - 1)){
      contentDiv.innerHTML +=     '<div style="text-align: center; font-size:20px">' + '<h6>Make sure to choose either A or B, before the next question.</h6>' + 
      'Click <b><span style="color:blue"> Next Page button </span></b> below to proceed to the next question set.' +
      '<p style="color:red"> DO NOT CLICK SUBMIT BUTTON! </p>' +
      '<label id="nextButton" class="btn btn-primary" onclick=showPage(' + (index + 1) + ')>Next Page</label>' +
      '</div>';
  }
  else{
      contentDiv.innerHTML += `
      <br><br>
      <div style="text-align: center; font-size:20px">
      <h6>Make sure to choose either A or B, before the next question.</h6>
      Click <b><span style="background-color:orange">Submit button</span></b> below to complete the HIT. Thank you. 
      </div>
    `;
  }
    // Populate the div with your specific content

    // Append this new div to the content area
    document.getElementById("contentArea").appendChild(contentDiv);

    const buttonA = document.getElementById('task_' + (index + 1) + '_buttonA');
    buttonA.addEventListener('click', function() {
      show_task_answer('task_' + (index + 1) + '_buttonA', 'task_' + (index + 1) + '_systemA_answer', data["System A"]);
    });
  
    // Add onclick event handler for System B
    const buttonB = document.getElementById('task_' + (index + 1) + '_buttonB');
    buttonB.addEventListener('click', function() {
      show_task_answer('task_' + (index + 1) + '_buttonB', 'task_' + (index + 1) + '_systemB_answer', data["System B"]);
    });
  }

  function showPage(index) {
    console.log("Attempting to show page:", index);

    // Only run this check when NOT on the first page
    if (currentPage !== 0) {
        // Get the radio buttons from the CURRENT page
        let radioA = document.getElementById("radioA_" + (currentPage + 1));
        let radioB = document.getElementById("radioB_" + (currentPage + 1));

        // Check if radioA and radioB are not null before checking their 'checked' properties
        if ((radioA && !radioA.checked) && (radioB && !radioB.checked)) {
            alert("Please make a selection before proceeding.");
            return; // exit the function early
        }
    }

    // Hide the current page
    let currentDiv = document.getElementById("page_" + currentPage);
    if (currentDiv) {
        currentDiv.style.display = "none";
    } else {
        console.error("Couldn't find div for current page:", currentPage);
    }

    // Show the new page
    let newDiv = document.getElementById("page_" + index);
    if (newDiv) {
        newDiv.style.display = "block";
    } else {
        console.error("Couldn't find div for new page:", index);
    }

    // Update currentPage
    currentPage = index;
}

function show_task(){

	document.getElementById('qual_page').style.display = "none";
	document.getElementById('task_page').style.display = "";

    const messageContainer = document.getElementById("task_page_head");
    messageContainer.innerHTML = `
    
    <h2>Task Round</h2>
		<p> For each question, your task is to <b>choose one answer </b> between the two systems in terms of the following point:
		<ul>
			<li>which system's answer <mark><b>aligns better</b></mark> and <mark><b> coherent </b></mark> with the instruction and reference sentences. (Please note that <b style="color:green">the reference answer is one possible answer to the instruction question.</b>) </li>
		</ul>
    <br>
    <h3><b style="color:red">ATTENTION</b>: Please be responsible for reading all instruction, reference, and two systems' outputs and answer thoroughly. Each set is not same with the previous question.</h3>
    <hr>
    `
    const exampleContainer = document.getElementById("example-container-task");
    exampleContainer.innerHTML = 
    `<div id="contentArea"">
     </div>
     `
     startPages();
}