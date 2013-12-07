  var csrftoken = $.cookie('csrftoken');
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type)) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
  function add_link(url_id, submit_id, url_group_id) {
  	var url = $(url_id);
  	var url_group = $(url_group_id);
  	var submit = $(submit_id);

	url.prop('disabled', true);
	submit.button('loading');

	var jqxhr = $.ajax({
	  type: "POST",
	  url: "/api/v1/link/",
	  contentType: 'application/json',
          data: JSON.stringify({"url": url.val()}),
	})
	.done(function() {
          submit.button('reset');
	  url.val('');
	  url.prop('disabled', false);
	  window.location.assign('/');
	})
	.fail(function() {
          submit.button('reset');
	  url.prop('disabled', false);
	  url_group.addClass('has-error');
	})
  }
