import fs from "fs";

export default async function() {
    const formationData = JSON.parse(fs.readFileSync("./src/services/formation.data.json", "utf-8"));
    return {
        instruments: formationData.instruments.map(instrument => ({
            gallery: {
                emoji: instrument.emoji,
                title: instrument.name,
                descr: instrument.shortDescription,
                href: instrument.hash
            },
            id: instrument.hash.slice(1), // remove the '#' for id usage
            emoji: instrument.emoji,
            name: instrument.name,
            teachers: instrument.teachers,
            styles: instrument.styles,
            longDescription: instrument.longDescription
        }))
    };
};