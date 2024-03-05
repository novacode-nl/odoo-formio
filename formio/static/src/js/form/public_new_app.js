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
            if (!!document.getElementById('formio_builder_uuid')) {
                this.builderUuid = document.getElementById('formio_builder_uuid').value;
            }
            this.configUrl = '/formio/public/form/new/' + this.builderUuid + '/config';
            this.submissionUrl = '/formio/public/form/new/' + this.builderUuid + '/submission';
            this.submitUrl = '/formio/public/form/new/' + this.builderUuid + '/submit';
            this.wizardSubmitUrl = '/formio/public/form/';
            this.apiUrl = '/formio/public/form/new/' + this.builderUuid + '/api';
            this.apiValidationUrl = this.apiUrl + '/validation';
        }

        publicSaveDraftDoneUrl() {
            return this.params.hasOwnProperty('public_save_draft_done_url') && this.params.public_save_draft_done_url;
        }

        publicSubmitDoneUrl() {
            return this.params.hasOwnProperty('public_submit_done_url') && this.params.public_submit_done_url;
        }

        isEmbed() {
            const url = new URL(window.location);
            const params = new URLSearchParams(url.search);
            return params.has('embed');
        }

        saveDraftDone(submission) {
            if (submission.state == 'draft') {
                if (this.publicSaveDraftDoneUrl()) {
                    const params = {save_draft_done_url: this.publicSaveDraftDoneUrl()};
                    if (window.self !== window.top) {
                        window.parent.postMessage({odooFormioMessage: 'formioSaveDraftDone', params: params});
                    }
                    else {
                        window.location = params.save_draft_done_url;
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

        submitDone(submission) {
            if (submission.state == 'submitted') {
                if (this.publicSubmitDoneUrl()) {
                    const params = {submit_done_url: this.publicSubmitDoneUrl()};
                    if (this.isEmbed()) {
                        window.parent.location = params.submit_done_url;
                    }
                    else if (window.self !== window.top) {
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

        saveDraftDone(submission) {
            if (submission.state == 'submitted') {
                if (this.publicSaveDraftDoneUrl()) {
                    const params = {save_draft_done_url: this.publicSaveDraftDoneUrl()};
                    if (window.self !== window.top) {
                        window.parent.postMessage({odooFormioMessage: 'formioSaveDraftDone', params: params});
                    }
                    else {
                        window.location = params.save_draft_done_url;
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

        scrollParent() {
            if (this.params.hasOwnProperty('scroll_into_view_selector')
                && this.params.scroll_into_view_selector) {
                const params = {
                    scroll_into_view_selector: this.params.scroll_into_view_selector
                };
                window.parent.postMessage({odooFormioMessage: 'formioScrollIntoView', params: params});
            }
        }

        getDataUrl(compObj) {
            return '/formio/public/form/new', self.formUuid, compObj.data.url;
        }
    }

    const app = new App();
    mount(App, document.getElementById('formio_form_app'));
}

async function start() {
    await whenReady();
    app();
};

start();
