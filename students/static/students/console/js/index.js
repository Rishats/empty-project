// =====================
// Create required vars
// =====================
var output = $('.output');
var input = $('textarea.input');
var toOutput;

// Creates the event listner for the comands ==
// Yes this is a long one - could do with some
// improvements ===============================
input.keypress(function(e) {
	if (e.which == 13) {
		var inputVal = $.trim(input.val());
		//console.log(inputVal);

		if (inputVal == "help") {
			help();
			input.val('');
		} else if (inputVal == "ping") {
			pong();
			input.val('');
		} else if (inputVal == "students") {
			StudentsShow();
			input.val('');
		} else if (inputVal == "clear") {
			clearConsole();
			input.val('');
		} else if (inputVal.startsWith("say") === true) {
			sayThis(inputVal);
			input.val('');
		} else if (inputVal.startsWith("sudo") === true) {
			sudo(inputVal);
			input.val('');
		} else if (inputVal == "time") {
			getTime();
			input.val('');
		} else if (inputVal == 'whats that sound' || inputVal == 'what\'s that sound' || inputVal == 'whats that sound?') {
			seperator();
			Output('<span class="blue">' + inputVal + '</span></br><span class="red">Machine Broken!</span></br>');
			seperator();
			input.val('');
		} else if (inputVal.startsWith("exit") === true) {
			Output('<span class="blue">Goodbye! Comeback soon.</span>');
		} else {
			console.log(inputVal);
			StudentWorkShow(inputVal);
		}
	}
});

// functions related to the commands typed
// =======================================

// prints out a seperator
function seperator() {
	Output('<span class="seperator">== == == == == == == == == == == == == == == == == ==</span></br>');
}

//clears the screen
function clearConsole() {
	output.html("");
	Output('<span>clear</span></br>');
}

// prints out a list of "all" comands available
function help() {
	var commandsArray = ['Help: Список доступных комманд',
		'>help - посмотреть команды',
		'>signup - пройти регистрацию',
		'>students - посмотреть студентов',
		'>ping - пингануть меня',
		'>time - узнать время',
		'>clear - почистить экран',
		'>say - сказать в консоль'];
	for (var i = 0; i < commandsArray.length; i++) {
		var out = '<span>' + commandsArray[i] + '</span><br/>'
		Output(out);
	}
}

// prints the result for the pong command
function pong() {
	Output('<span>pong</span></br><span class="pong"><b class="left">|</b><b class="right">|</b></span></br>');
}

// function to the say command
function sayThis(data) {
	data = data.substr(data.indexOf(' ') + 1);
	Output('<span class="green">[say]:</span><span>' + data + '</span></br>');
}

// sudo?!? not really
function sudo(data) {
	data = data.substr(data.indexOf(' ') + 1);
	if (data.startsWith("say") === true) {
		data = "Не не! " + data + " У тебя нет прав!"
	} else if (data.startsWith("apt-get") === true) {
		data = "<span class='green'>Проверка...</span> Спасибо конечно, но все обновляется моим создателем (Ришатом!)..."
	} else {
		data = "The force is week within you, my master you not be!"
	}
	Output('<span>' + data + '</span></br>');
}

// function to get current time...not
function getTime() {
	Output('<span>It\'s the 21st century man! Get a SmartWatch</span></br>');
}


function StudentsShow() {
	var studentsArray = ['>Студенты:', '>Напиши свой логин чтобы войти в свою СУБД!:', 'rishat', 'khairidin', 'vlad', 'fara'];
	seperator();
	for (var i = 0; i < studentsArray.length; i++) {
		var out = '<span>' + studentsArray[i] + '</span><br/>'
		Output(out);
	}
	seperator();
}

function StudentWorkShow(inputVal) {
	var studentsArray = ['>Students:', 'rishat', 'khairidin', 'vlad', 'fara'];
    studentsArray.some(function(student) {
		if(inputVal.startsWith(student)) {
			Output('<span class="blue">OKAY! YOU WILL REDIRECT!.</span>');
			setTimeout(function() {
				window.open('/phpmyadmin/index.php?db='+student);
			}, 1000);
			return true;
		}
		else{
			Output('<span>COMMAND NOT FOUND</span></br>');
			input.val('');
			return false;
		}
	});
}

// Prints out the result of the command into the output div
function Output(data) {
	$(data).appendTo(output);
}