// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

$(document).ready(function() {
    iFrameResize({}, '.formio_form_embed');

    window.addEventListener('message', function(event) {
        var base_url = window.location.protocol + '//' + window.location.host;
        if (event.origin == base_url && event.data == 'formioSubmitDone') {
            var portal_submit_done_url = document.getElementById('portal_submit_done_url');
            if (portal_submit_done_url && portal_submit_done_url.value.length > 0) {
                window.location = portal_submit_done_url;
            }
            else {
                window.location.reload();
            }
        }
    }, false);
});
