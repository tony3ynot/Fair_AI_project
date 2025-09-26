import React from 'react';
import { biasColors, biasLabels } from '../utils/bias';

interface BiasSpectrumProps {
  currentBias?: string;
  biasScore?: number;
}

export const BiasSpectrum: React.FC<BiasSpectrumProps> = ({ currentBias, biasScore }) => {
  const biasOrder = ['left', 'center-left', 'center', 'center-right', 'right'];
  
  // Convert bias score (-1 to 1) to position (0 to 100)
  const getPositionFromScore = (score: number) => {
    return ((score + 1) / 2) * 100;
  };

  const position = biasScore !== undefined ? getPositionFromScore(biasScore) : null;

  return (
    <div className="w-full">
      <div className="relative h-8 rounded-full overflow-hidden bg-gray-200">
        <div className="absolute inset-0 flex">
          {biasOrder.map((bias) => (
            <div
              key={bias}
              className="flex-1 h-full"
              style={{ backgroundColor: biasColors[bias] }}
            />
          ))}
        </div>
        
        {position !== null && (
          <div
            className="absolute top-1/2 -translate-y-1/2 w-1 h-10 bg-black rounded-full"
            style={{ left: `${position}%`, transform: 'translate(-50%, -50%)' }}
          >
            <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 text-xs font-medium whitespace-nowrap">
              {biasScore?.toFixed(2)}
            </div>
          </div>
        )}
      </div>
      
      <div className="flex justify-between mt-2">
        {biasOrder.map((bias) => (
          <span
            key={bias}
            className={`text-xs ${currentBias === bias ? 'font-bold' : ''}`}
            style={{ color: currentBias === bias ? biasColors[bias] : '#6b7280' }}
          >
            {biasLabels[bias]}
          </span>
        ))}
      </div>
    </div>
  );
};