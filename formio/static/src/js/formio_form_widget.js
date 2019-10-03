// Copyright Nova Code (http://www.novacode.nl)
// See LICENSE file for full licensing details.

odoo.define('formio.formio_form', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var QWeb = core.qweb;
    var _t = core._t;

    var FormioForm = AbstractAction.extend({
        title: core._t('Form.io Form'),

        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.action_manager = parent;
            this.params = params;

            // Adding values from the context is necessary to put this information in the url via the action manager so that
            // you can retrieve it if the person shares his url or presses f5
            _.each(params.params, function (value, name) {
                params.context[name] = name.indexOf('_ids') !== -1 ? _.map((value+'').split(), parseFloat) : value;
            });
        },

        start: function() {
            var self = this;
            var form_id = self.params.context.active_id;

            var form = this._rpc({
                model: 'formio.form',
                method: 'search_read',
                args: [[['id', '=', form_id]]],
            }).then(function (res) {
                self.form = res.length && res[0];
                self.$el.html(QWeb.render("FormioFormWidget", {'widget': self}));
            });
            return $.when(form, this._super.apply(this, arguments));
        }
    });

    core.action_registry.add('formio_form', FormioForm);
    return FormioForm;
});
