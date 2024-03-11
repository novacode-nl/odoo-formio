// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

$(document).ready(function() {
    iFrameResize({}, '.formio_form_embed');

    window.addEventListener('message', function(event) {
        const baseUrl = window.location.protocol + '//' + window.location.host;

        if (event.data.hasOwnProperty('odooFormioMessage')) {
            const msg = event.data.odooFormioMessage,
                  params = event.data.params,
                  submitDoneUrl = params.hasOwnProperty('submit_done_url') && params.submit_done_url,
                  saveDraftDoneUrl = params.hasOwnProperty('save_draft_done_url') && params.save_draft_done_url,
                  scrollIntoViewSelector = params.hasOwnProperty('scroll_into_view_selector') && params.scroll_into_view_selector;

            if (event.origin == baseUrl && msg == 'formioSubmitDone' && submitDoneUrl) {
                window.location = submitDoneUrl;
            }
            else if (event.origin == baseUrl && msg == 'formioSaveDraftDone' && saveDraftDoneUrl) {
                window.location = saveDraftDoneUrl;
            }
            else if (event.origin == baseUrl && msg == 'formioScrollIntoView' && scrollIntoViewSelector) {
                document.querySelector(scrollIntoViewSelector, window.parent.parent.document).scrollIntoView();
            }
            else if (event.origin == baseUrl && msg == 'formioScrollTop') {
                window.parent.scrollTo(0, 0);
            }
        }
    }, false);
});
