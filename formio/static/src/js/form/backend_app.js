// Copyright Nova Code (https://www.novacode.nl)
// See LICENSE file for full licensing details.

function uuidv4() {
    // Used in cache invalidation (can also be used in PWA).
    // TODO: DRY, move to generic function/method to be imported here.
    // XXX: not ideal https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(
        /[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

// random importPath ensures no caching
let importPath = "./formio_form.js?" + uuidv4();
let { OdooFormioForm } = await import(importPath);

// use global owl
// can't import from "@odoo/owl", because not an @odoo-module
const { mount, whenReady, xml } = owl;

function app() {
    class App extends OdooFormioForm {
        static template = xml`
            <div t-name="App">
                <div id="formio_form"></div>
            </div>
        `;

        initForm() {
            if (!!document.getElementById('formio_form_uuid')) {
                this.formUuid = document.getElementById('formio_form_uuid').value;
            }
            this.configUrl = '/formio/form/' + this.formUuid + '/config';
            this.submissionUrl = '/formio/form/' + this.formUuid + '/submission';
            this.submitUrl = '/formio/form/' + this.formUuid + '/submit';
            this.wizardSubmitUrl = '/formio/form/';
            this.isPortalUrl = window.location.pathname.indexOf('/formio/portal/') >= 0;
            this.apiUrl = '/formio/form/' + this.formUuid + '/api';
            this.apiValidationUrl = this.apiUrl + '/validation';
        }

        portalSaveDraftDoneUrl() {
            return this.params.hasOwnProperty('portal_save_draft_done_url') && this.params.portal_save_draft_done_url;
        }

        portalSubmitDoneUrl() {
            return this.params.hasOwnProperty('portal_submit_done_url') && this.params.portal_submit_done_url;
        }

        saveDraftDone(submission) {
            if (submission.state == 'draft') {
                if (this.isPortalUrl && this.portalSaveDraftDoneUrl()) {
                    const params = {save_draft_done_url: this.portalSaveDraftDoneUrl()};
                    if (window.self !== window.top) {
                        window.parent.postMessage({odooFormioMessage: 'formioSaveDraftDone', params: params});
                    }
                    else {
                        window.location = params.submit_done_url;
                    }
                }
                else {
                    setTimeout(function() {
                        window.location.reload();
                    }, 500);
                }
            }
            else {
                setTimeout(function() {
                    window.location.reload();
                }, 500);
            }
        }

        submitDone(submission) {
            if (submission.state == 'submitted') {
                if (this.isPortalUrl && this.portalSubmitDoneUrl()) {
                    const params = {submit_done_url: this.portalSubmitDoneUrl()};
                    if (window.self !== window.top) {
                        window.parent.postMessage({odooFormioMessage: 'formioSubmitDone', params: params});
                    }
                    else {
                        window.location = params.submit_done_url;
                    }
                }
                else {
                    setTimeout(function() {
                        window.location.reload();
                    }, 500);
                }
            }
            else {
                setTimeout(function() {
                    window.location.reload();
                }, 500);
            }
        }

        scrollParent() {
            window.parent.postMessage({odooFormioMessage: 'formioScrollTop', params: {}});
        }
    }

    const app = new App();
    mount(App, document.getElementById('formio_form_app'));
}

async function start() {
    await whenReady();
    app();
}

start();
