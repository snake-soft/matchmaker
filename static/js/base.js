function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	// Needed for POST forms with Ajax in Django (XSRF-Protection)
	beforeSend : function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function loadLadderRealtime(){
	$.get("/realtime/team/",{
	}).done(function(data) {
		$("#match-realtime").html(data);
	});
};

function loadMatchRealtime() {
	if ($('#id_firstteam').val() && $('#id_secondteam').val() && $('#id_firstteam').val() != $('#id_secondteam').val()){
		$.get("/realtime/team/",{
			firstteam: $('#id_firstteam').find(":selected").val(),
			secondteam: $('#id_secondteam').find(":selected").val(),
			firstteam_goals: $('#id_firstteam_goals').val(),
			secondteam_goals: $('#id_secondteam_goals').val(),
		}).done(function(data) {
			$("#match-realtime").html(data);
		});
	}
};

function increment(element){
	$(element).get(0).value++;
	loadMatchRealtime();
}

function decrement(element){
	if ($(element).val() > 0){
		$(element).get(0).value--;
		loadMatchRealtime();
	}
}

$(document).ready(function() {
	loadDataTables();
    
    $('#id_firstteam,#id_secondteam,#id_firstteam_goals,#id_secondteam_goals').on('change',function(){
    	loadMatchRealtime()
	});
} );

