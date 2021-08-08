// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.
// See formio.js.LICENSE.txt in this directory, for attribution.

$(document).ready(function() {
    var Component = Formio.Components.components.button;

    class OdooReCaptchaButtonComponent extends Component {

        static schema(...extend) {
            return super.schema({
                "label": "Submit",
                "key": "odoo_recaptcha_button",
                "type": "odoo_recaptcha_button",
            }, ...extend);
        }

        static get builderInfo() {
            return {
                title: 'reCAPTCHA Button (odoo)',
                group: 'advanced',
                icon: 'stop',
                weight: 1100,
                documentation: '#',
                schema: this.schema()
            };
        }

        triggerReCaptcha() {
            if (!this.root) {
                return;
            }
            const recaptchaComponent = this.root.components.find((component) => {
                return component.component.type === 'odoo_recaptcha';
                    //component.component.eventType === 'buttonClick' &&
                    //component.component.buttonKey === this.component.key;
            });
            if (recaptchaComponent) {
                recaptchaComponent.verify(`${this.component.key}Click`);
            }
        }
    }

    Formio.Components.addComponent('odoo_recaptcha_button', OdooReCaptchaButtonComponent);
});
