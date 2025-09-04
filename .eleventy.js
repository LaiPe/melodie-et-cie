export default async function(eleventyConfig) {
    // Copier les assets statiques - spécification explicite
    eleventyConfig.addPassthroughCopy("assets/**/*");
    eleventyConfig.addPassthroughCopy("assets/css/**/*");
    
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
