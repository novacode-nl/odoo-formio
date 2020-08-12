// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

$(document).ready(function() {
    var Component = Formio.Components.components.recaptcha;

    class OdooReCaptchaComponent extends Component {

        static schema(...extend) {
            return super.schema({
                "label": "(odoo) reCAPTCHA",
                "key": "odoo_recaptcha",
                "type": "odoo_recaptcha",
                "input": true
            }, ...extend);
        }

        static get builderInfo() {
            return {
                title: '(odoo) reCAPTCHA',
                group: 'advanced',
                icon: 'refresh',
                weight: 1010,
                documentation: '#',
                schema: this.schema()
            };
        }

        verify(actionName) {
            const siteKey = this.component.site_key;
            if (!siteKey) {
                console.error('There is no Site Key specified in API-settings of the (odoo) reCAPTCHA component');
                return;
            }

            this.odooRecaptchaVerifiedPromise = new Promise(function (resolve, reject) {
                grecaptcha.ready(function() {
                    grecaptcha.execute(siteKey, {action: actionName}).then(function(token) {
                        // sendVerificationRequest
                        const verify_url = '/formio/public/recaptcha';
                        $.jsonRpc.request(verify_url, 'call', {'token': token}).then(function(verificationResult) {
                            return resolve(verificationResult);
                        });
                    });
                });
            });
        }

        beforeSubmit() {
            if (this.odooRecaptchaVerifiedPromise) {
                return this.odooRecaptchaVerifiedPromise.then(function(res) {
                    if (!res.success) {
                        alert('reCAPTCHA verification failed');
                        console.warning('reCAPTCHA verification failed');
                        event.preventDefault();
                    }
                });
            }
            else {
                return super.beforeSubmit();
            }
        }
    }

    OdooReCaptchaComponent.editForm = function(a,b,c) {
        var form = Component.editForm(a,b,c);
        var tabs = form.components.find(obj => {return obj.type === "tabs";});
        var datatab = tabs.components.find(obj => {return obj.key == 'api';});
        // Remove multiple components. I could probably make it work... but nah
        datatab.components.splice(datatab.components.findIndex(obj=>{return obj.key = "multiple";}),1);
        var site_key = {
            "input": true,
            "key": "site_key",
            "label": "Site Key (reCAPTCHA)",
            "type": "textfield",
        };
        datatab.components.splice(0 ,0, site_key);
        return form;
    };

    Formio.Components.addComponent('odoo_recaptcha', OdooReCaptchaComponent);
});
