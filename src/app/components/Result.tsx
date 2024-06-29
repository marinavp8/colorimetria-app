import { CloudArrowUpIcon, LockClosedIcon, ServerIcon } from '@heroicons/react/20/solid'



const estaciones = {
    Primavera: [
        { name: "Spring" },
        { subtono: "frío" },
        { features: "lala1" },
        { colores: ["azul", "rojo"] },
        { metales: ["plata"] },
        { photo: "/spring.jpeg" },
    ],
    Verano: [
        { name: "Summer" },
        { subtono: "frío" },
        { features: "lala2" },
        { colores: ["azul", "rojo"] },
        { metales: ["plata"] },
        { photo: "/summer.jpeg" },
    ],
    Otoño: [
        { name: "Autumn" },
        { subtono: "cálido" },
        { features: "lala3" },
        { colores: ["azul", "rojo"] },
        { metales: ["plata"] },
        { photo: "/autumn.jpeg" },
    ],
    Invierno: [
        { name: "Winter" },
        { subtono: "cálido" },
        { features: "lala4" },
        { colores: ["azul", "rojo"] },
        { metales: ["plata"] },
        { photo: "/winter.jpeg" },
    ],
}
interface ResultProps {
    result: Feature;
}

type Feature = "Primavera" | "Verano" | "Otoño" | "Invierno"

export default function Result2({ result }: ResultProps) {
    console.log(result)
    let featuresToDisplay = estaciones[result] || []
    console.log("featuresToDisplay", featuresToDisplay)

    return (
        <div className="overflow-hidden bg-white py-24 sm:py-32">
            {featuresToDisplay.map((feature: any) => (
                <div className="mx-auto max-w-7xl md:px-6 lg:px-8">
                    <div className="grid grid-cols-1 gap-x-8 gap-y-16 sm:gap-y-20 lg:grid-cols-2 lg:items-start">
                        <div className="px-6 lg:px-0 lg:pr-4 lg:pt-4">
                            <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-lg">
                                {/* <h2 className="text-base font-semibold leading-7 text-indigo-600">Your best colors</h2> */}
                                <p className="mt-2 text-xl font-hatton tracking-tight text-gray-900 sm:text-xl">Here they are</p>
                                {/* <p className="mt-6 text-lg leading-8 text-gray-600">
                                lalala
                            </p> */}
                                <dl className="mt-10 max-w-xl space-y-8 text-base leading-7 text-gray-600 lg:max-w-none">
                                    <div key={feature.features} className="relative pl-9">
                                        <dt className="inline font-semibold text-gray-900">
                                            {feature.subtono}
                                        </dt>{' '}
                                        <dd className="">{feature.features}</dd>
                                        <dd className="">{feature.features}</dd>
                                        <dd className="">
                                            {feature.colores && feature.colores.map((color: any) => {
                                                return <p>{color}</p>;
                                            })}
                                        </dd>
                                        <dd className="">
                                            {feature.metales && feature.metales.map((metal: any) => {
                                                return <p>{metal}</p>;
                                            })}
                                        </dd>
                                    </div>
                                </dl>
                            </div>
                        </div>
                        <div className="sm:px-6 lg:px-0">
                            <div className="relative isolate overflow-hidden bg-indigo-500 px-6 pt-8 sm:mx-auto sm:max-w-2xl sm:rounded-3xl sm:pl-16 sm:pr-0 sm:pt-16 lg:mx-0 lg:max-w-none">
                                <div
                                    className="absolute -inset-y-px -left-3 -z-10 w-full origin-bottom-left skew-x-[-30deg] bg-indigo-100 opacity-20 ring-1 ring-inset ring-white"
                                    aria-hidden="true"
                                />
                                <div className="mx-auto max-w-2xl sm:mx-0 sm:max-w-none">
                                    <img
                                        src={feature.photo}
                                        alt="Product screenshot"
                                        width={2432}
                                        height={1442}
                                        className="-mb-12 w-[57rem] max-w-none rounded-tl-xl bg-gray-800 ring-1 ring-white/10"
                                    />
                                </div>
                                <div
                                    className="pointer-events-none absolute inset-0 ring-1 ring-inset ring-black/10 sm:rounded-3xl"
                                    aria-hidden="true"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}
