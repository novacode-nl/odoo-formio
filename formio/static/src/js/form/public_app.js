// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

import { OdooFormioForm } from "./formio_form.js";

/**
FIX / WORKAROUND (known) browser incompatibility errors.
Wrap Component class and bootstrap into functions.

OS/platform: browsers
=====================
- Mac: Safari 13.1
- iOS: Safari, Chrome

Errors
======
- Safari 13.1 on Mac experiences error:
  unexpected token '='. expected an opening '(' before a method's parameter list
- iOS not debugged yet. Dev Tools not present in browser.
*/

function app() {
    class App extends OdooFormioForm {
        initForm() {
            if (!!document.getElementById('formio_form_uuid')) {
                this.form_uuid = document.getElementById('formio_form_uuid').value;
            }

            this.config_url = '/formio/public/form/' + this.form_uuid + '/config';
            this.submission_url = '/formio/public/form/' + this.form_uuid + '/submission';
            this.submit_url = '/formio/public/form/' + this.form_uuid + '/submit';
        }
    }
    const app = new App();
    app.mount(document.getElementById('formio_form_app'));
}

async function start() {
    const templates = await owl.utils.loadFile('/formio/static/src/js/form/public_app.xml');
    const env = { qweb: new owl.QWeb({templates})};
    owl.Component.env = env;
    await owl.utils.whenReady();
    app();
}

start();
