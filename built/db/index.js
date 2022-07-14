"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cosmos_1 = require("@azure/cosmos");
const config_1 = require("../config");
class Database {
    client;
    databaseId;
    containers;
    container;
    constructor(databaseId = 'OrganiseMyMeals') {
        this.client = new cosmos_1.CosmosClient({ endpoint: config_1.azureEndpointUri, key: config_1.azurePrimaryKey });
        this.databaseId = databaseId;
        this.containers = { mealContainer: null, userContainer: null };
    }
    async init() {
        const dbResponse = await this.client.databases.createIfNotExists({ id: this.databaseId });
        const { container: mealContainer } = await dbResponse.database.containers.createIfNotExists({
            id: "meal",
            partitionKey: "/id"
        });
        const { container: userContainer } = await dbResponse.database.containers.createIfNotExists({
            id: "user",
            partitionKey: "/id"
        });
        this.containers = { mealContainer, userContainer };
    }
    async query(queryString) {
        try {
            const querySpec = { query: queryString };
            const { resources } = await this.container.items.query(querySpec).fetchAll();
            return resources;
        }
        catch (error) {
            console.log(error);
        }
    }
    async getMeal(id) {
        try {
            const querySpec = {
                query: "SELECT * FROM c WHERE c.id = @id AND c.type = 'meal'",
                parameters: [
                    { name: "@id", value: id }
                ]
            };
            // read all items in the Items container
            const { resources: items } = await this.containers.mealContainer.items
                .query(querySpec)
                .fetchAll();
            return items[0];
        }
        catch (error) {
            console.log(error);
        }
    }
    async getMeals() {
        try {
            const querySpec = { query: "SELECT * FROM c WHERE c.type = 'meal'" };
            const { resources } = await this.containers.mealContainer.items
                .query(querySpec).fetchAll();
            return resources;
        }
        catch (error) {
            console.log(error);
        }
    }
    async getMealTag(id) {
        const querySpec = {
            query: "SELECT * FROM c WHERE c.type = @type AND c.id = @id",
            parameters: [
                { name: "@id", value: id },
                { name: "@type", value: "mealtag" },
            ]
        };
        const { resources: [mealTag] } = await this.containers.mealContainer.items
            .query(querySpec).fetchAll();
        return mealTag;
    }
    async getMealTags() {
        const querySpec = {
            query: "SELECT * FROM c WHERE c.type = @type",
            parameters: [
                { name: "@type", value: "mealtag" },
            ]
        };
        const { resources } = await this.containers.mealContainer.items
            .query(querySpec).fetchAll();
        return resources;
    }
    async addMeals(item) {
        try {
            const response = await this.containers.mealContainer.items.create(item);
            return response;
        }
        catch (error) {
            console.log(error);
        }
    }
    async editMeal(modifiedMeal) {
        try {
            const response = await this.containers.mealContainer
                .item(modifiedMeal.id, modifiedMeal.id)
                .replace(modifiedMeal);
            return response;
        }
        catch (error) {
            console.log(error);
        }
    }
    async deleteMeal(id) {
        try {
            const response = await this.containers.mealContainer.item(id, id).delete();
            return response;
        }
        catch (error) {
            console.log(error);
        }
    }
    async deleteMeals(ids) {
        try {
            // TODO: Delete all items in array
            console.log("WARNING: Only deleting first item in array, TODO: Delete all items in array");
            const response = await this.containers.mealContainer.item(ids[0], ids[0]).delete();
            return response;
        }
        catch (error) {
            console.log(error);
        }
    }
    async getUser(id) {
        try {
            const querySpec = {
                query: "SELECT * FROM u WHERE u.id = @id",
                parameters: [
                    { name: "@id", value: id }
                ]
            };
            const { resources } = await this.containers.userContainer.items
                .query(querySpec)
                .fetchAll();
            return resources[0];
        }
        catch (error) {
            console.log(error);
        }
    }
}
exports.default = Database;
