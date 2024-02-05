function show_qual() {

    document.getElementById('instruction_page').style.display = "none";
	document.getElementById('qual_page').style.display = "";
	const messageContainer = document.getElementById("qual_page");
	messageContainer.innerHTML = `

    <h2>Qualification Round</h2>
    <hr>
		<p> For each question, your task is to <b>choose one answer </b> between the two systems in terms of the following point:
		<ul>
			<li>which system's answer <mark><b>aligns better</b></mark> and <mark><b> coherent </b></mark> with the instruction and reference sentences. (Please note that <b style="color:green">the reference answer is one possible answer to the instruction question.</b>) </li>
		</ul>
    <br>
    <h2>Set 1</h2>
    <hr>
        <div id="qual_1" style="border-style: dotted; border-color: CornflowerBlue; padding: 10px; color:black">
            <p>### <b> Question: </b> Which system's answer is <b style='color:SlateBlue'>more coherent</b>, considering the reference and instruction sentences? </p>
            <ul>
                <li> <b>The instruction</b>: What would be some etiquette norms to keep in mind when invited to a business party? </li>
                <li> <b>The reference</b>: Follow the dress code and be on time.</li>
            </ul>
            <p> Here are two answers from System A and B, respectively: 

            <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <th style="text-align: center; width: 200px;"> System A</th>
                <th style="text-align: center; width: 200px;"> System B</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>Dress conventionally and professionally. Wear suites and ties for men, and business attire for women. </td>
                <td>Begin your meal before the host starts. </td>
            </tr>
            </tbody>
            </table>
            <h4 style="text-align:center">The coolest thing that System A can do is a 60 second handstand.</h4>
            <br>
            <p style="text-align: center">
            <mark>
            Please choose which system's answer aligns and cohere better with the instruction and reference sentences?
            </mark>
            </p>
            <div style="text-align: center">
            <label class="btn btn-success btn-lg">
                <input type="radio" name="qual_1" value="A"> System A
            </label>
            <label class="btn btn-info btn-lg">
                <input type="radio" name="qual_1" value="B"> System B
            </label>
            </div>

        </div>
    <br>
    <h2>Set 2</h2>
    <hr>
        <div id="qual_2" style="border-style: dotted; border-color: CornflowerBlue; padding: 10px; color:black">
            <p>### <b> Question: </b> Which system's answer is <b style='color:SlateBlue'>more coherent</b>, considering the reference and instruction sentences? </p>
            <ul>
                <li> <b>The instruction</b>: What are the two ways that I can improve my writing skills in Spanish? </li>
                <li> <b>The reference</b>: Take some online courses that teach writing skills in English, or read many Spanish books. </li>
            </ul>
            <p> Here are two answers from System A and B, respectively: 

            <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <th style="text-align: center; width: 200px;"> System A</th>
                <th style="text-align: center; width: 200px;"> System B</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td> Read many books that are written in Spanish and hone your speaking skill about pronunciation. </td>
                <td> You may take a tutoring class that teaches the professional writing in Spanish.</td>
            </tr>
            </tbody>
            </table>

            <h4 style="text-align:center">System A plays a lot of soccer and basketball.</h4>
            <br>
            <p style="text-align: center">
            <mark>
            Please choose which system's answer aligns and cohere better with the instruction and reference sentences?
            </mark>
            </p>
            <div style="text-align: center">
            <label class="btn btn-success btn-lg">
                <input type="radio" name="qual_2" value="A"> System A
            </label>
            <label class="btn btn-info btn-lg">
                <input type="radio" name="qual_2" value="B"> System B
            </label>
            </div>

        </div>        
    <br>
    <h2>Set 3</h2>
        <hr>
            <div id="qual_3" style="border-style: dotted; border-color: CornflowerBlue; padding: 10px; color:black">
                <p>### <b> Question: </b> Which system's answer is <b style='color:SlateBlue'>more coherent</b>, considering the reference and instruction sentences? </p>
                <ul>
                    <li> <b>The instruction</b>: When did Queen Elizabeth II of United Kingdom pass away? </li>
                    <li> <b>The reference</b>: She passed away on September 2022. </li>
                </ul>
                <p> Here are two answers from System A and B, respectively: 
    
                <table class="table table-bordered table-striped">
                <thead>
                <tr>
                    <th style="text-align: center; width: 200px;"> System A</th>
                    <th style="text-align: center; width: 200px;"> System B</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td> The Queen Elizabeth II of Great Britain died in 2022. </td>
                    <td> Queen Elizabeth II of UK was born in 1926. </td>
                </tr>
                </tbody>
                </table>

                <h4 style="text-align:center">System B has been all around Europe two times.</h4>
                <br>
                <p style="text-align: center">
                <mark>
                Please choose which system's answer aligns and cohere better with the instruction and reference sentences?
                </mark>
                </p>
                <div style="text-align: center">
                <label class="btn btn-success btn-lg">
                    <input type="radio" name="qual_3" value="A"> System A
                </label>
                <label class="btn btn-info btn-lg">
                    <input type="radio" name="qual_3" value="B"> System B
                </label>
                </div>
    
            </div>        

        <br>

        <div id='submit_qual_answer'>    
            <p style='text-align: center; font-size:20px'><b>Click <span style="color: green">Check Answers</span></b> button to check your answers. 
            <b>DO NOT CLICK <span style="background-color:orange">SUBMIT</span> BUTTON!</b>
            <br><br>   
            <button id="start_button" class="btn btn-success" onclick="submitAnswer_qual()">Check Answers</button>
            </p>
        </div>

        <div id="qual_result" class="mt-3"></div>
	
	`
	document.getElementById('instruction_page').style.display = "none";
	document.getElementById('qual_page').style.display = "";
	document.getElementById('task_page').style.display = "none";
}

function submitAnswer_qual() {
    const messageContainer = document.getElementById("qual_result");

    const q1Value = document.querySelector('input[name="qual_1"]:checked').value;
    const q2Value = document.querySelector('input[name="qual_2"]:checked').value;
    const q3Value = document.querySelector('input[name="qual_3"]:checked').value;
    
    if (q1Value === "A" && q2Value === "B" && q3Value === "A") {
        messageContainer.innerHTML = `
            <div class="alert alert-success mt-3" role="alert">
                Hooray! You understand the objective of our study and are qualified for the real task! 
            </div>
            <br>
            <div id="go_to_task" style="text-align: center"> 
            <b>Click <span style="color: blue">Start Task</span></b> button to proceed to the real task. 
            <br>
            <div class="alert alert-warning mt-3" role="alert">
            <b style="color:red"> ATTENTION! </b> To approve your HIT, we plan to review your answers from the next tasks later. If you do not meet certain criteria, your work may be rejected. 
            By clicking the 'Start Task' button, you are considered to have agreed to the above.
            </div>
            <br>
            <button id="start_button" class="btn btn-primary" onclick="show_task()">Start Task</button>
            </div>
        `;
        document.getElementById("submit_qual_answer").style.display = "none";
        document.getElementById("go_to_task").style.display = "";
    } else {
        messageContainer.innerHTML = `
            <div class="alert alert-danger mt-3" role="alert">
                Wrong answer. Please read through all three sets carefully and try again. 
            </div>
        `;
    }
    document.getElementById("go_to_task").style.display = "block";
}