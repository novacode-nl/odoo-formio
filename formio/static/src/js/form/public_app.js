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
            this.configUrl = '/formio/public/form/' + this.formUuid + '/config';
            this.submissionUrl = '/formio/public/form/' + this.formUuid + '/submission';
            this.submitUrl = '/formio/public/form/' + this.formUuid + '/submit';
            this.wizardSubmitUrl = '/formio/public/form/';
            this.apiUrl = '/formio/public/form/' + this.formUuid + '/api';
            this.apiValidationUrl = this.apiUrl + '/validation';
        }

        publicSubmitDoneUrl() {
            return this.params.hasOwnProperty('public_submit_done_url') && this.params.public_submit_done_url;
        }

        submitDone(submission) {
            if (submission.state == 'submitted') {
                if (this.publicSubmitDoneUrl()) {
                    const params = {submit_done_url: this.publicSubmitDoneUrl()};
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
                    }, 1000);
                }
            }
            else {
                setTimeout(function() {
                    window.location.reload();
                }, 1000);
            }
        }
    }

    scrollParent() {
        if (this.params.hasOwnProperty('scroll_into_view_selector')
            && this.params.scroll_into_view_selector) {
            const params = {
                scroll_into_view_selector: this.params.scroll_into_view_selector
            };
            window.parent.postMessage({odooFormioMessage: 'formioScrollIntoView', params: params});
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
