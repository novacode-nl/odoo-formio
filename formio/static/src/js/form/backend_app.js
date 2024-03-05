// Copyright Nova Code (https://www.novacode.nl)
// See LICENSE file for full licensing details.

const { protectComponent, uuidv4 } = await import('./utils.js');

// random import path ensures no caching
const pathBranding = "./branding.js?" + uuidv4();
const pathForm = "./formio_form.js?" + uuidv4();

let { Branding } = await import(pathBranding);
let { OdooFormioForm } = await import(pathForm);

// use global owl
// can't import from "@odoo/owl", because not an @odoo-module
const { mount, whenReady, xml } = owl;

function app() {
    class App extends OdooFormioForm {
        static components = { Branding }
        static template = xml`
            <div t-name="App">
                <div id="formio_form"></div>
                <Branding getData="this.getData"/>
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

    protectComponent(App);
    const app = new App();
    mount(App, document.getElementById('formio_form_app'));
}

async function start() {
    await whenReady();
    app();
}

start();
