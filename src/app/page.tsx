import Head from 'next/head';
import ImageUpload from '@/app/components/ImageUpload';

export default function Home() {
  return (
    <div>
      <div className="relative bg-white">
        <div className="mx-auto max-w-7xl  lg:gap-x-8 lg:px-8">
          <div className="px-6 pb-24 pt-10 sm:pb-32 lg:px-0 lg:pb-56 lg:pt-48 ">
            <div className="mx-auto lg:mx-0 flex flex-col lg:flex-row">
              <div>
                <h1 className="mt-24 text-2xl font-hatton2 tracking-tight text-gray-900 sm:mt-10 sm:text-4xl">
                  We use edgy technology to identify your colours and metals                </h1>
                <p className="mt-6 font-fahkwang text-lg leading-8 text-gray-600">
                  Introduce a face photo to determine your colorimetry.
                </p>
                <div className='mt-7'>
                  <ImageUpload />
                </div>
              </div>

            </div>
          </div>
          {/* <div className="relative lg:col-span-5 lg:-mr-8 xl:absolute xl:inset-0 xl:left-1/2 xl:mr-0">
            <img
              className="aspect-[3/2] w-full bg-gray-50 object-cover lg:absolute lg:inset-0 lg:aspect-auto lg:h-full"
              src="video/prueba.gif"
              alt=""
            />
          </div> */}
        </div>
      </div>
      {/* <Head>
        <title>Colorimetría App</title>
      </Head> */}
    </div>
  );
}
