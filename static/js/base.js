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

function loadDataTables(sort, direction, firstColRanking=false){
    var t = $('.datatable').DataTable( {
    	"columnDefs": [ {
    		"searchable": false,
    		"orderable": true,
    		"targets": 0
    	} ],
    	"order": [[ sort, direction]]
    } );
    if (firstColRanking){
    	t.on( 'order.dt search.dt', function () {
    		t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
    			cell.innerHTML = i+1;
    		} );
    	} ).draw();
    }
}

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

function setPopover() {
	$('[data-toggle="popover"]').popover({
		html: true,
		content: function(){
			return $(this).find('.popover-content').html();
		}
	})
}

$(document).ready(function() {
	$('#id_firstteam,#id_secondteam,#id_firstteam_goals,#id_secondteam_goals').on('change',function(){
		loadMatchRealtime()
	});
	setPopover()
});
