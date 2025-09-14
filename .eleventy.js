export default async function(eleventyConfig) {
    // Copier les assets statiques
    eleventyConfig.addPassthroughCopy("src/assets");
    
    // Watchers pour rebuild automatique
    eleventyConfig.addWatchTarget("src/assets");
    eleventyConfig.addWatchTarget("src/**/*.11tydata.json");
    eleventyConfig.addWatchTarget("src/**/*.11tydata.js");

    // Filtres personnalisés
    eleventyConfig.addFilter("date", function(value) {
        return new Date(value).toLocaleDateString('fr-FR');
    });

    eleventyConfig.addFilter("map", function(array, key) {
        console.log("Mapping on :", array, "with key:", key);
        if (!Array.isArray(array) || typeof key !== "string") {
            console.warn("Invalid arguments for 'map' filter");
            return [];
        }
        console.log(`Mapping array of length ${array.length} by key '${key}'`);
        const result = array.map(item => item[key]);
        console.log("Mapped result:", result);
        return result;
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
