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

function loadMatchRealtime() {
	$.get("/realtime/team/",{
		firstteam: $('#id_firstteam').find(":selected").val(),
		secondteam: $('#id_secondteam').find(":selected").val(),
		firstteam_goals: $('#id_firstteam_goals').val(),
		secondteam_goals: $('#id_secondteam_goals').val(),
	}).done(function(data) {
		$("#match-realtime").html(data);
	});
};

function loadDataTables(){
    var t = $('#player-overview').DataTable( {
        "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0
        } ],
        "order": [[ 1, 'asc' ]]
    } );
 
    t.on( 'order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
}

$(document).ready(function() {
	loadDataTables();
    
    $('#id_firstteam,#id_secondteam,#id_firstteam_goals,#id_secondteam_goals').on('change',function(){
    	loadMatchRealtime()
	});
} );

