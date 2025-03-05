function getURLVar(key) {
	var value = [];

	var query = String(document.location).split('?');

	if (query[1]) {
		var part = query[1].split('&');

		for (i = 0; i < part.length; i++) {
			var data = part[i].split('=');

			if (data[0] && data[1]) {
				value[data[0]] = data[1];
			}
		}

		if (value[key]) {
			return value[key];
		} else {
			return '';
		}
	}
}

$(document).ready(function() {
	//Form Submit for IE Browser
	
	// tooltips on hover
	$('[data-toggle=\'tooltip\']').tooltip({container: 'body', html: true});

	// Makes tooltips work on ajax generated content
	$(document).ajaxStop(function() {
		$('[data-toggle=\'tooltip\']').tooltip({container: 'body'});
	});

	// https://github.com/opencart/opencart/issues/2595
	$.event.special.remove = {
		remove: function(o) {
			if (o.handler) {
				o.handler.apply(this, arguments);
			}
		}
	}
	
	// tooltip remove
	$('[data-toggle=\'tooltip\']').on('remove', function() {
		$(this).tooltip('dispose');
	});

	
	
	$('#button-menu').on('click', function(e) {
		e.preventDefault();
		
		$('#column-left').toggleClass('active');
	});

	// Set last page opened on the menu
	$('#menu a[href]').on('click', function() {
		sessionStorage.setItem('menu', $(this).attr('href'));
	});


	// Image Manager
	$(document).on('click', 'a[data-toggle=\'image\']', function(e) {
		var $element = $(this);
		var $popover = $element.data('bs.popover'); // element has bs popover?

		e.preventDefault();

		// destroy all image popovers
		$('a[data-toggle="image"]').popover('dispose');

		// remove flickering (do not re-add popover when clicking for removal)
		if ($popover) {
			return;
		}

		$element.popover({
			html: true,
			placement: 'right',
			title:'lichup',
			trigger: 'manual',
			content4:'<a href="javascript:void("0") id="button-image" class="btn btn-primary"><i class="fa fa-pencil"></i></a>',
			content: function() {
				return '<a href="javascript:void("0")  id="button-image" class="btn btn-primary"><i class="fa fa-pencil"></i></a> <a href="javascript:void("0")  id="button-clear" class="btn btn-danger"><i class="fa fa-trash-o"></i></a>';
			}
		});

		$element.popover('show');

		$('#button-image').on('click', function() {
			var $button = $(this);
			var $icon   = $button.find('> i');

			$('#modal-image').remove();

			$.ajax({
				//url: 'http://localhost:8000/admin/fm/faltumodel/common_filemanager?k=1' + '&target=' + $element.parent().find('input').attr('id') + '&thumb=' + $element.attr('id'),
				url: '/admin/fm/faltumodel/common_filemanager?k=1' + '&target=' + $element.parent().find('input').attr('id') + '&thumb=' + $element.attr('id'),
				dataType: 'html',
				beforeSend: function() {
					$button.prop('disabled', true);
					if ($icon.length) {
						$icon.attr('class', 'fa fa-circle-o-notch fa-spin');
					}
				},
				complete: function() {
					$button.prop('disabled', false);

					if ($icon.length) {
						$icon.attr('class', 'fa fa-pencil');
					}
				},
				success: function(html) {
					$('body').append('<div id="modal-image" class="modal">' + html + '</div>');

					$('#modal-image').modal('show');
				}
			});

			$element.popover('dispose');
		});

		$('#button-clear').on('click', function() {
			$element.find('img').attr('src', $element.find('img').attr('data-placeholder'));

			$element.parent().find('input').val('');

			$element.popover('dispose');
		});
	});
});

// Autocomplete */
