// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

import { OdooFormioForm } from "./formio_form.js";

const { xml } = owl.tags;
const { whenReady } = owl.utils;

class App extends OdooFormioForm {
    static template = xml`<div/>`;

    setUrls() {
        this.config_url = '/formio/public/form/create/' + this.builder_uuid + '/config';
        this.submission_url = false;
        this.submit_url = '/formio/public/form/create/' + this.builder_uuid + '/submit';
    }
}

function setup() {
    const app = new App();
    app.mount(document.body);
}

whenReady(setup);
