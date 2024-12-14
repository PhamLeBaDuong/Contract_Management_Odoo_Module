/** @odoo-module */
import { registry } from "@web/core/registry";
import { CustomController } from "./custom_controller";
import { CustomArchParser } from "./custom_arch_parser";
import { CustomModel } from "./custom_model";
import { CustomRenderer } from "./custom_renderer";

export const customView = {
    type: "custom_view",
    display_name: "Custom",
    icon: "fa fa-picture-o",
    multiRecord: true,
    Controller: CustomController,
    ArchParser: CustomArchParser,
    Model: CustomModel,
    Renderer: CustomRenderer,
    // ... other properties
};

registry.category("views").add("custom_view", customView);
