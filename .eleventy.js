import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

export default async function(eleventyConfig) {
    // Copier les assets statiques
    eleventyConfig.addPassthroughCopy("src/assets");

    // Copie du dossier admin
    eleventyConfig.addPassthroughCopy("src/admin");
    
    // Watchers pour rebuild automatique
    eleventyConfig.addWatchTarget("src/assets");
    eleventyConfig.addWatchTarget("src/admin");
    eleventyConfig.addWatchTarget("src/**/*.11tydata.json");
    eleventyConfig.addWatchTarget("src/**/*.11tydata.js");

    // Filtres personnalisés
    eleventyConfig.addFilter("date", function(value) {
        if (!value) return "";
        let date;
        if (value instanceof Date) {
            date = value;
        } else {
            date = new Date(value);
            if (isNaN(date)) return value;
        }
        // Format : JJ/MM/AAAA HH:MM
        return date.toLocaleDateString('fr-FR', { year: 'numeric', month: '2-digit', day: '2-digit' }) +
            ' ' +
            date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    });

    eleventyConfig.addFilter("map", function(array, key) {
        // console.log("Mapping on :", array, "with key:", key);
        if (!Array.isArray(array) || typeof key !== "string") {
            console.warn("Invalid arguments for 'map' filter");
            return [];
        }
        // console.log(`Mapping array of length ${array.length} by key '${key}'`);
        const result = array.map(item => item[key]);
        // console.log("Mapped result:", result);
        return result;
    });
    
    // Collection personnalisée pour les formations
    eleventyConfig.addCollection("formations", async (collectionsApi) => {
        // Résoudre le chemin absolu du dossier
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const dir = path.join(__dirname, "src/services/formation");

        return fs.readdirSync(dir)
            .filter(file => file.endsWith(".json"))
            .map(file => {
                // console.log("Loading formation data from:", file);
                const data = JSON.parse(fs.readFileSync(path.join(dir, file), "utf-8"));
                // console.log("Loaded formation data:", data);
                data.__filename = file; // optionnel, pour debug ou liens
                return data;
            })
            .map(data => ({
                gallery: {
                    emoji: data.emoji,
                    title: data.name,
                    descr: data.shortDescription,
                    href: data.hash
                },
                hash: data.hash,
                emoji: data.emoji,
                name: data.name,
                teachers: data.teachers,
                styles: data.styles,
                longDescription: data.longDescription
            }));
    });

    // Collection personnalisée pour les évenements à venir
    eleventyConfig.addCollection("upcoming_events", (collectionsApi) => {
        // Résoudre le chemin absolu du dossier
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const dir = path.join(__dirname, "src/services/evenements/upcoming");

        return fs.readdirSync(dir)
            .filter(file => file.endsWith(".json"))
            .map(file => {
                // console.log("Loading formation data from:", file);
                const data = JSON.parse(fs.readFileSync(path.join(dir, file), "utf-8"));
                // console.log("Loaded formation data:", data);
                data.__filename = file; // optionnel, pour debug ou liens
                return data;
            });
    });
    
    // Configuration des dossiers de sortie
    return {
        dir: {
            input: "src",
            output: "_site",
            includes: "_includes"
        },
        templateFormats: ["njk", "md", "html"],
        markdownTemplateEngine: "njk",
        htmlTemplateEngine: "njk",
        dataTemplateEngine: "njk"
    };
};
