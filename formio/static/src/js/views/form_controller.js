/** @odoo-module **/

var FormController = require("web.FormController");
FormController.include({
    /**
    HACK
    It's not recommended to override with include (in-place overwrite).
    However extend doesn't work here!
    https://stackoverflow.com/questions/49891397/odoo-difference-in-javascript-extend-and-include#49893168

    The core _onSwitchView (AbstractController) doesn't obtain and set
    the res_id in the event data.  This ensures the RecordView
    implementations work now!
    **/
    _onSwitchView: function (ev) {
        //ev.stopPropagation();
        if (ev.target.viewType == 'form') {
            var env = this.model.get(ev.target.handle, {raw: true});
            ev.data.res_id = env.res_id;
        }
        ev.data.controllerID = this.controllerID;
    },
});
