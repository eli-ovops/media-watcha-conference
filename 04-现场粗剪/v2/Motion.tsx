// Exact INT02-v2 portrait derivative; same source image / camera / single aperture.
import React from 'react';
import {registerRoot,Composition} from 'remotion';
import {NewsSpotlightFocus} from './NewsFocusPortrait';
export function BoardFocus(){return <NewsSpotlightFocus src="P08.jpg" sourceWidth={5712} sourceHeight={4284} regions={[{x:.50,y:.335,width:.455,height:.32}]} order="camera-first" focusAt={.55} cameraSeconds={1.1} emphasisAt={1.95} zoom={2.12} dimOpacity={.60} returnAt={10} returnSeconds={1.35}/>;}
export const Root=()=> <Composition id="BoardFocus" component={BoardFocus} durationInFrames={240} fps={60} width={1080} height={1920}/>;
registerRoot(Root);
