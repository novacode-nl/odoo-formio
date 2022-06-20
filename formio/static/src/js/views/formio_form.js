/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { standardViewProps } from "@web/views/helpers/standard_view_props";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";

const { Component } = owl;

var viewRegistry = registry.category("views");

class FormModel extends Model {
    static services = ["orm"];

    setup(params, { orm }) {
        this.model = params.resModel;
        this.resId = params.resId;
        this.fields = params.fields;
        this.orm = orm;
        this.keepLast = new KeepLast();
    }

    async load(params) {
        this.data = await this.keepLast.add(
            this.orm.searchRead(this.model, [["id", "=", this.resId]], this.fields)
        );
        this.notify();
    }
}

class FormRenderer extends Component {
    setup() {
        this.model = this.props.model;
        //this.l10n = localization;
        //this.formioBuilder = null;
    }
}

class FormView extends Component {
    setup() {
        this.model = useModel(FormModel, {
            resModel: this.props.resModel,
            resId: this.props.resId,
            // TODO fields
            fields: [] // eg: ['id', 'name']
        });
    }
};

FormModel.services = ["orm"];

FormView.components = { Layout };
FormView.display_name = "FormView";
FormView.icon = "fa-rocket";
FormView.multiRecord = false;
FormView.props = {
    ...standardViewProps,
};
FormView.template = "formio.form";
FormView.type = "formio_form";

viewRegistry.add('formio_form', FormView);
