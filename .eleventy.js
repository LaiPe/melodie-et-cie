export default async function(eleventyConfig) {
    // Copier les assets statiques
    eleventyConfig.addPassthroughCopy("src/assets");
    
    // Watchers pour rebuild automatique
    eleventyConfig.addWatchTarget("src/assets");
    eleventyConfig.addWatchTarget("src/**/*.11tydata.json");

    // Filtres personnalisés
    eleventyConfig.addFilter("date", function(value) {
        return new Date(value).toLocaleDateString('fr-FR');
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
