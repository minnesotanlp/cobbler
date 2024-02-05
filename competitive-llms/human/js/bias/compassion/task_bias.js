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
    contentDiv.id = `page_${index}`;
    contentDiv.style.display = "none"; // Hidden by default
    contentDiv.innerHTML = `
    <h3> Question Set ${index + 1} out of ${A.length}</h3>
    <br>
    <div id="task_${index + 1}" style="border-style: dotted; border-color: CornflowerBlue; padding: 10px; color:black">
      <p>### <b> Question: </b> Which system's answer is <b style='color:SlateBlue'>more coherent</b>, considering the reference and instruction sentences? </p>
      <ul>
        <li> <b>The instruction</b>: <span id="instruction_${index + 1}">${data.instruction}</span> </li>
        <li> <b>The reference</b>: <span id="reference_${index + 1}">${data.reference}</span></li>
      </ul>
      <p> Here are two answers from System A and B, respectively: </p>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th style="text-align: center; width: 200px;"> System A</th>
            <th style="text-align: center; width: 200px;"> System B</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td id="systemA_${index + 1}">${data["System A"]}</td>
            <td id="systemB_${index + 1}">${data["System B"]}</td>
          </tr>
        </tbody>
      </table>
      <p style="text-align: center">
      <mark>
      Please choose which system's answer aligns and cohere better with the instruction and reference sentences?
      </mark>
      </p>
      <div style="text-align: center">
        <label class="btn btn-success btn-lg">
          <input type="radio" id="radioA_${index + 1}" name="task_${index + 1}" value="A"> System A
        </label>
        <label class="btn btn-info btn-lg">
          <input type="radio" id="radioB_${index + 1}" name="task_${index + 1}" value="B"> System B
        </label>
      </div>
    </div>
  `;
    // Create a new div for this page
    if (index != (A.length - 1)){
        contentDiv.innerHTML += `
        <div style="text-align: center; font-size:20px">
        Click <b><span style="color:blue"> Next Page button </span></b> below to proceed to the next question set. 
        <p style="color:red"> DO NOT CLICK SUBMIT BUTTON! </p>
        <label id="nextButton" class="btn btn-primary" onclick=showPage(${index + 1})>Next Page</label>
        </div>
        `;
    }
    else{
        contentDiv.innerHTML += `
        <br><br>
        <div style="text-align: center; font-size:20px">
        Click <b><span style="background-color:orange">Submit button</span></b> below to complete the HIT. Thank you. 
        </div>
      `;
    }  
    // Populate the div with your specific content

    // Append this new div to the content area
    document.getElementById("contentArea").appendChild(contentDiv);
  }

function showPage(index) {

    document.getElementById(`page_${currentPage}`).style.display = "none";
    // Show the new page
    document.getElementById(`page_${index}`).style.display = "block";
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
    <hr>
    `
    const exampleContainer = document.getElementById("example-container-task");
    exampleContainer.innerHTML = 
    `<div id="contentArea"">
     </div>
     `
     startPages();
}