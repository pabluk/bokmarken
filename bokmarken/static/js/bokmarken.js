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

$(document).on('toggleLinkPublic', function(event, btnElement, states) {
    card = btnElement.parents("div[id|='card-link']");
    link_id = card.attr("id").replace("card-link-", "");
    button = $('> span', btnElement);
    is_public = button.hasClass(states.on);
	var jqxhr = $.ajax({
        type: "PATCH",
        url: "/api/v1/link/" + link_id + "/",
        contentType: 'application/json',
            data: JSON.stringify({"is_public": !is_public}),
    })
    if (is_public) {
        button.removeClass(states.on).addClass(states.off);
    } else {
        button.removeClass(states.off).addClass(states.on);
    }
})

$(document).on('toggleLinkArchived', function(event, btnElement, states) {
    card = btnElement.parents("div[id|='card-link']");
    link_id = card.attr("id").replace("card-link-", "");
    button = $('> span', btnElement);
    is_archived = button.hasClass(states.on);
	var jqxhr = $.ajax({
        type: "PATCH",
        url: "/api/v1/link/" + link_id + "/",
        contentType: 'application/json',
            data: JSON.stringify({"is_archived": !is_archived}),
    })
    if (is_archived) {
        button.removeClass(states.on).addClass(states.off);
    } else {
        button.removeClass(states.off).addClass(states.on);
    }
    card.hide();
})
