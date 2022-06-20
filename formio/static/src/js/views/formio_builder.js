/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { standardViewProps } from "@web/views/helpers/standard_view_props";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";

const { Component } = owl;

const viewRegistry = registry.category("views");

class BuilderModel extends Model {
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

class BuilderRenderer extends Component {
    setup() {
        this.model = this.props.model;
        //this.l10n = localization;
        //this.formioBuilder = null;
    }
}

class BuilderView extends Component {
    setup() {
        this.model = useModel(BuilderModel, {
            resModel: this.props.resModel,
            resId: this.props.resId,
            // TODO fields
            fields: [] // eg: ['id', 'name']
        });
    }
};

BuilderModel.services = ["orm"];

BuilderView.components = { Layout };
BuilderView.display_name = "BuilderView";
BuilderView.icon = "fa-rocket";
BuilderView.multiRecord = false;
BuilderView.props = {
    ...standardViewProps,
};
BuilderView.template = "formio.builder";
BuilderView.type = "formio_builder";

viewRegistry.add('formio_builder', BuilderView);
