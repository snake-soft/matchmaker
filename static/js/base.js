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
		},
		title : function(){
			return $(this).attr('data-title') + '<button onclick="$(this).closest(\'div.popover\').popover(\'hide\');" type="button" class="close" aria-hidden="true">&times;</button>';
		},
		trigger: 'manual'
	});
	$('[data-toggle="popover"]').click(function(){
		$(this).popover('show');
	});
	/* Workaround for checkboxes inside popover */
	$('[data-toggle="popover"]').popover().find('label').click(function(){
		var id = $(this).attr('for');
		var box = $('#' + id);
		if (box.attr("checked") == "checked"){
			$('#' + id).attr( "checked", false );
		} else {
			$('#' + id).attr( "checked", true );
		}
	});
}

function setPopoverLazy() {
	$('[data-toggle="popover-lazy"]').popover({
	    html: true,
	    content: function(){
	        var div_id =  "tmp-id-" + $.now();
	        return details_in_popup($(this).attr('data-href'), div_id);
	    }
	});
}
function details_in_popup(link, div_id){
    $.ajax({
        url: link,
        success: function(response){
            $('#'+div_id).html(response);
        }
    });
    return '<div id="'+ div_id +'">Loading...</div>';
}

/* Tracker Funktion */
$(document).ready(function() {
	$('#new-match-form').submit(function() {
		   return confirm("Is the game really finished and ready for saving?");
	});
	$('.middle').click(function(){
		var x = $('#id_firstteam').find(":selected").val()
		$('#id_firstteam').val($('#id_secondteam').find(":selected").val());
		$('#id_secondteam').val(x);

		x = $('#id_firstteam_goals').val()
		$('#id_firstteam_goals').val($('#id_secondteam_goals').val());
		$('#id_secondteam_goals').val(x);
		loadMatchRealtime();
	});
	$('#id_firstteam,#id_secondteam,#id_firstteam_goals,#id_secondteam_goals').on('change',function(){
		loadMatchRealtime()
	});
});

/* For All */
$(document).ready(function() {
	setPopover()
	setPopoverLazy()
});
